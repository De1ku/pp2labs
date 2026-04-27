from pathlib import Path

import psycopg2
from config import DB_CONFIG

BASE_DIR = Path(__file__).resolve().parent


def connect():
    return psycopg2.connect(**DB_CONFIG)


def run_sql_file(filename: str):
    with open('./'+filename, "r", encoding="utf-8") as f:
        sql = f.read()

    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)


def init_db():
    # Сначала схема, затем функции и процедуры
    run_sql_file("schema.sql")
    run_sql_file("functions.sql")
    run_sql_file("procedures.sql")
