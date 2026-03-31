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