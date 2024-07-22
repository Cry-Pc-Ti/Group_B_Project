import sqlite3

def content(c,text):
    cur = c.cursor()
    try:
        cur.execute("INSERT INTO contents (content) VALUES(?)",(text,))
        c.commit()
        return True
    except sqlite3.IntegrityError:
        return False