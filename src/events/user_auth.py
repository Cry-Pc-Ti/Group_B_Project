import sqlite3


def register_user(conn, user_id, password):
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO users (user, password) VALUES (?, ?)", (user_id, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False


def login_user(conn, user_id, password):
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE user=? AND password=?", (user_id, password))
    user = cur.fetchone()
    if user:
        return user[0]
    else:
        return None
