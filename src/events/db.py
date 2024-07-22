import sqlite3

def user_db(conn):
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

def content_db(c):
    cur = c.cursor()
    cur.execute(
            """
        CREATE TABLE IF NOT EXISTS contents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL
        )
        """
    )
    c.commit()