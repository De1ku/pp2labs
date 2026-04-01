import psycopg2
from config import DB_CONFIG


def connect():
    return psycopg2.connect(**DB_CONFIG)


def init_db():
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS phonebook (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(100) UNIQUE NOT NULL,
                    phone VARCHAR(20) UNIQUE NOT NULL
                )
            """)

            # если таблица осталась с Practice7, добавим surname
            cur.execute("""
                ALTER TABLE phonebook
                ADD COLUMN IF NOT EXISTS surname VARCHAR(100)
            """)


def run_sql_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        sql = f.read()

    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)