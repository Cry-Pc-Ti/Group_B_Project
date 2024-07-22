import sqlite3
import streamlit as st
from events.content import content
from events.db import content_db

# 内容のDB接続
c = sqlite3.connect("static/db/content.db")
content_db(c)

def main_screen(c):
    st.title("title")

    if st.button("Logout"):
        st.session_state["screen"] = "login"
        st.rerun()

    # 文章入力
    with st.form("contents", clear_on_submit=True):
        text = st.text_area("contents")

        if st.form_submit_button("Submit"):
            content(c,text)
            st.success("complete")

    if st.button("WordCloud"):
        st.session_state["screen"] = "word"
        st.rerun()