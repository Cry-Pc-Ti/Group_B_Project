import streamlit as st
from sqlite3 import Connection
from events.user_auth import register_user


def register_screen(conn: Connection):
    st.title("ユーザ登録")

    user_id = st.text_input("ID")
    password = st.text_input("パスワード", type="password")
    if st.button("登録"):
        if register_user(conn, user_id, password):
            st.success("ユーザ登録が完了しました。ログイン画面に移動します。")
            st.session_state["current_screen"] = "ログイン"
            st.rerun()
        else:
            st.error("このIDは既に使用されています")
