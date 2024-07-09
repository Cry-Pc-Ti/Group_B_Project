import os
import sqlite3


def create_connection(db_name):
    db_path = os.path.join("static", "db", f"{db_name}.db")
    conn = sqlite3.connect(db_path)
    return conn


def create_user_tables(conn):
    cur = conn.cursor()
    cur.execute(
        """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
    """
    )
    conn.commit()


def create_diary_tables(conn):
    cur = conn.cursor()
    cur.execute(
        """
    CREATE TABLE IF NOT EXISTS diaries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        date TIMESTAMP NOT NULL,
        icon TEXT NOT NULL,
        content TEXT NOT NULL,
        sleep_start TIMESTAMP NOT NULL,
        sleep_end TIMESTAMP NOT NULL,
        create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    )
    conn.commit()
