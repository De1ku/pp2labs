import psycopg2

from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD


class Database:
    """Класс для работы с PostgreSQL: игроки, игровые сессии и таблица лидеров."""

    def __init__(self):
        self.connection = None
        self.error = None
        self.connect()

    def connect(self):
        """Подключается к базе и создаёт таблицы, если их ещё нет."""
        try:
            self.connection = psycopg2.connect(
                host=DB_HOST,
                port=DB_PORT,
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
            self.connection.autocommit = True
            self.create_tables()
        except Exception as error:
            # Игра не падает, если база временно недоступна.
            # На экране лидерборда будет показано сообщение об ошибке.
            self.connection = None
            self.error = str(error)

    def create_tables(self):
        """Создаёт таблицы players и game_sessions по требованиям задания."""
        if self.connection is None:
            return

        with self.connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS players (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS game_sessions (
                    id SERIAL PRIMARY KEY,
                    player_id INTEGER NOT NULL REFERENCES players(id) ON DELETE CASCADE,
                    score INTEGER NOT NULL,
                    level INTEGER NOT NULL,
                    played_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

    def get_or_create_player(self, username):
        """Возвращает id игрока. Если такого username нет, создаёт нового игрока."""
        if self.connection is None:
            return None

        username = username.strip() or "Player"

        with self.connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO players (username)
                VALUES (%s)
                ON CONFLICT (username) DO UPDATE SET username = EXCLUDED.username
                RETURNING id;
            """, (username,))
            return cursor.fetchone()[0]

    def save_game_session(self, username, score, level):
        """Сохраняет результат игры после Game Over."""
        if self.connection is None:
            return False

        player_id = self.get_or_create_player(username)

        with self.connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO game_sessions (player_id, score, level)
                VALUES (%s, %s, %s);
            """, (player_id, score, level))

        return True

    def get_personal_best(self, username):
        """Возвращает лучший результат конкретного игрока."""
        if self.connection is None:
            return 0

        username = username.strip() or "Player"

        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT COALESCE(MAX(gs.score), 0)
                FROM game_sessions gs
                JOIN players p ON p.id = gs.player_id
                WHERE p.username = %s;
            """, (username,))
            return cursor.fetchone()[0]

    def get_leaderboard(self, limit=10):
        """Возвращает Top-10 результатов из базы данных."""
        if self.connection is None:
            return []

        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT p.username, gs.score, gs.level, TO_CHAR(gs.played_at, 'YYYY-MM-DD HH24:MI')
                FROM game_sessions gs
                JOIN players p ON p.id = gs.player_id
                ORDER BY gs.score DESC, gs.level DESC, gs.played_at ASC
                LIMIT %s;
            """, (limit,))
            return cursor.fetchall()
