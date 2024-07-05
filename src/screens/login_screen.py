import streamlit as st
from events.user_auth import login_user


def login_screen(conn):
    st.title("ログイン")

    # ユーザ登録ボタンを右上に配置
    col1, col2 = st.columns([5, 1])
    with col1:
        pass
    with col2:
        if st.button("ユーザ登録"):
            st.session_state["current_screen"] = "ユーザ登録"
            st.rerun()

    user_id = st.text_input("ID")
    password = st.text_input("パスワード", type="password")

    if st.button("ログイン"):
        user_id = login_user(conn, user_id, password)
        if user_id:
            st.session_state["user_id"] = user_id
            st.session_state["current_screen"] = "日記登録"
            st.rerun()
        else:
            st.error("IDまたはパスワードが間違っています")
