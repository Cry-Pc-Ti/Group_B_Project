from datetime import timedelta
import streamlit as st
from events.diary_operations import get_diary_entries
from events.generate_wordcloud import generate_wordcloud


def word_cloud_screen(conn):
    # ユーザIDの取得
    user_id = st.session_state["user_id"]
    if not user_id:
        st.error("ログインしてください")
        st.session_state["current_screen"] = "ログイン"
        st.rerun()

    start_of_week = st.session_state["start_of_week"].date()

    # タイトル
    st.title("ワードクラウド")

    with st.spinner("ワードクラウドを生成中..."):
        # 今週の日記を取得し結合
        diaries = get_diary_entries(conn, user_id)
        weekly_content = ""
        for i in range(7):
            date = start_of_week + timedelta(days=i)
            diary = next((diary for diary in diaries if diary["date"].date() == date), None)
            if diary:
                weekly_content += diary["content"] + "\n"
        wordcloud = generate_wordcloud(weekly_content)
        st.pyplot(wordcloud)
