import sqlite3
from typing import Generator

DB_PATH = "figurinhas.db"


def init_db() -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS figurinhas (
                id         INTEGER  PRIMARY KEY AUTOINCREMENT,
                numero     TEXT     NOT NULL,
                nome       TEXT     NOT NULL,
                selecao    TEXT     NOT NULL,
                tipo       TEXT     NOT NULL,
                posicao    TEXT     NOT NULL,
                created_at DATETIME NOT NULL,
                updated_at DATETIME NOT NULL
            )
        """)
        conn.commit()


def get_db() -> Generator[sqlite3.Connection, None, None]:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()
