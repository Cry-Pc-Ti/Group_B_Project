from datetime import datetime


def add_diary_entry(conn, user_id, date, icon, content, active_start, active_end):
    c = conn.cursor()
    c.execute(
        "INSERT INTO diaries (user_id, date, icon, content, active_start, active_end) VALUES (?, ?, ?, ?, ?, ?)",
        (user_id, date, icon, content, active_start, active_end),
    )
    conn.commit()


def get_diary_entries(conn, user_id):
    c = conn.cursor()
    c.execute("SELECT * FROM diaries WHERE user_id=?", (user_id,))
    rows = c.fetchall()
    diaries = []
    for row in rows:
        diary = {
            "id": row[0],
            "user_id": row[1],
            "date": datetime.strptime(row[2], "%Y-%m-%d %H:%M:%S.%f"),
            "icon": row[3],
            "content": row[4],
            "active_start": row[5],
            "active_end": row[6],
            "create_at": row[7],
        }
        diaries.append(diary)
    return diaries


def get_diary_by_date(conn, user_id, date):
    c = conn.cursor()
    c.execute("SELECT * FROM diaries WHERE user_id=? AND date(date)=date(?)", (user_id, date))
    row = c.fetchone()
    if row:
        diary = {
            "id": row[0],
            "user_id": row[1],
            "date": datetime.strptime(row[2], "%Y-%m-%d %H:%M:%S.%f"),
            "icon": row[3],
            "content": row[4],
            "active_start": row[5],
            "active_end": row[6],
            "create_at": row[7],
        }
        return diary
    return None
