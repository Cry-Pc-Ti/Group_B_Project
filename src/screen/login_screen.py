import sqlite3
import streamlit as st


# SQLiteデータベースに接続
def get_user_data(username):
    path = "static/db/users.db"
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user_data = cursor.fetchone()
    conn.close()
    return user_data


# ユーザー名とパスワードをチェック
def login(username, password):
    user_data = get_user_data(username)
    if user_data and user_data[1] == password:
        return True
    return False


def login_page():
    st.title("Login Page")

    # ログインフォーム
    st.sidebar.title("Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    login_button = st.sidebar.button("Login")

    if login_button:
        if login(username, password):
            st.success("Login successful!")
            st.write(f"Welcome, {username}!")
            # ログイン成功後に表示したいページや機能をここに追加
            st.write("This is the main content of the app.")
        else:
            st.error("Invalid username or password")


if __name__ == "__main__":
    login_page()
