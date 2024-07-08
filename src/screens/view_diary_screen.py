import streamlit as st
from datetime import datetime, time, timedelta
from events.diary_operations import get_diary_by_date

st.markdown(
    """
    <style>
        .st-du {
            color : #00000000
        }
        .st-ea {
            color : #00000000
        }
    </style>
    """,
    unsafe_allow_html=True,
)


def view_diary_screen(conn):
    if "user_id" in st.session_state:
        user_id = st.session_state["user_id"]
        selected_date = st.session_state["selected_date"]
        today = datetime.now().date()

        # 日記がすでに存在するかチェック
        existing_diary = get_diary_by_date(conn, user_id, selected_date.strftime("%Y-%m-%d"))
        if not existing_diary:
            st.session_state["current_screen"] = "日記登録"
            st.experimental_rerun()

        # ボタンを配置
        col1, col2, col3 = st.columns([6, 1, 1])
        with col1:
            back_button = st.button("一覧に戻る")
            if back_button:
                back_to_calendar()
        with col2:
            if st.button("前の日"):
                st.session_state["selected_date"] -= timedelta(days=1)
                st.experimental_rerun()
        with col3:
            if selected_date < today:
                if st.button("次の日"):
                    st.session_state["selected_date"] += timedelta(days=1)
                    st.experimental_rerun()

        # 日記の内容を表示
        st.title(selected_date.strftime("%Y/%m/%d"))

        diary = get_diary_by_date(conn, user_id, selected_date)
        if diary:
            emoji = ["🥰", "😊", "😑", "😥", "😓"]
            selected_emoji = emoji.index(diary["icon"])
            st.selectbox("感情", ["🥰", "😊", "😑", "😥", "😓"], index=selected_emoji)

            st.text_area("内容", value=diary["content"])

            sleep_start = diary["sleep_start"]
            sleep_end = diary["sleep_end"]

            col1, col2 = st.columns(2)
            with col1:
                st.time_input("就寝", value=time(sleep_start.hour, sleep_start.minute), step=timedelta(minutes=30))
            with col2:
                st.time_input("起床", value=time(sleep_end.hour, sleep_end.minute), step=timedelta(minutes=30))

    else:
        st.error("ログインしてください")
        st.session_state["current_screen"] = "ログイン"
        st.experimental_rerun()


def back_to_calendar():
    st.session_state["current_screen"] = "カレンダー"
    st.rerun()
