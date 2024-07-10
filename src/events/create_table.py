import sqlite3

# SQLiteデータベースに接続
# 相対パスから絶対パスを取得
path = "static/db/users.db"
conn = sqlite3.connect(path)
cursor = conn.cursor()

# usersテーブルを作成
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT NOT NULL
)
"""
)

# コミットして接続を閉じる
conn.commit()
conn.close()
