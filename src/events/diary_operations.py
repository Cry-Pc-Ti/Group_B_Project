from datetime import date, datetime
from sqlite3 import Connection
from typing import List, Optional
from models.diary import Diary


def add_diary_entry(conn: Connection, diary: Diary):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO diaries (user_id, date, icon, content, sleep_start, sleep_end) VALUES (?, ?, ?, ?, ?, ?)",
        (
            f"{diary.user_id}",
            f"{diary.date}",
            f"{diary.icon}",
            f"{diary.content}",
            f"{diary.sleep_start}",
            f"{diary.sleep_end}",
        ),
    )
    conn.commit()


def get_diary_entries(conn: Connection, user_id: int) -> List[Diary]:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM diaries WHERE user_id=?", (f"{user_id}"))
    rows = cursor.fetchall()
    diaries = []
    for row in rows:
        diary = Diary(
            id=row[0],
            user_id=row[1],
            date=datetime.strptime(row[2], "%Y-%m-%d").date(),
            icon=row[3],
            content=row[4],
            sleep_start=datetime.strptime(row[5], "%Y-%m-%d %H:%M:%S"),
            sleep_end=datetime.strptime(row[6], "%Y-%m-%d %H:%M:%S"),
            create_at=row[7],
        )
        diaries.append(diary)
    return diaries


def get_diary_by_date(conn: Connection, user_id: int, date: date) -> Optional[Diary]:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM diaries WHERE user_id=? AND date=?", (f"{user_id}", f"{date}"))
    row = cursor.fetchone()
    if row:
        return Diary(
            id=row[0],
            user_id=row[1],
            date=datetime.strptime(row[2], "%Y-%m-%d").date(),
            icon=row[3],
            content=row[4],
            sleep_start=datetime.strptime(row[5], "%Y-%m-%d %H:%M:%S"),
            sleep_end=datetime.strptime(row[6], "%Y-%m-%d %H:%M:%S"),
            create_at=row[7],
        )
    return None
