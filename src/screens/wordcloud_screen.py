import streamlit as st
from datetime import date, timedelta
from events.diary_operations import get_diary_by_date
from events.generate_wordcloud import generate_wordcloud


def wordcloud_screen(conn):
    user_id: int = st.session_state["user_id"]
    start_of_week: date = st.session_state["start_of_week"]

    # タイトル
    st.title("ワードクラウド")

    # 選択された週の初めの日付
    start_of_week: date = st.session_state["start_of_week"]

    # 今週の各日付を取得
    week_days = [start_of_week + timedelta(days=i) for i in range(7)]

    # 週を前後に移動するためのボタン
    col1, col2, col3 = st.columns([8, 1.5, 2])
    with col1:
        st.subheader(f"{start_of_week.strftime('%m/%d')} - {week_days[-1].strftime('%m/%d')}")
    with col2:
        if st.button("前の週"):
            st.session_state["start_of_week"] -= timedelta(days=7)
            st.rerun()
    with col3:
        if st.button("次の週"):
            st.session_state["start_of_week"] += timedelta(days=7)
            st.rerun()

    is_loaded = False

    with st.spinner("ワードクラウドを生成中..."):

        weekly_content = ""

        for day in week_days:
            diary = get_diary_by_date(conn, user_id, day)

            if diary:
                weekly_content += diary.content + "\n"

        if weekly_content:
            # ワードクラウドを作成・表示
            wordcloud = generate_wordcloud(weekly_content)
            is_loaded = True

        else:
            st.warning("今週の日記がありません")
            st.stop()

    if is_loaded:
        st.pyplot(wordcloud)
