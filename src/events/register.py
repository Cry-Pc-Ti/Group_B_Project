import sqlite3

def register(conn,id,password):
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO users (user, password) VALUES(?,?)",(id,password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False