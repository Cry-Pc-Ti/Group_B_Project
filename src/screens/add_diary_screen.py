import datetime
import streamlit as st
from events.diary_operations import add_diary_entry


def add_diary_screen(conn, date):
    if "user_id" in st.session_state:
        back_button = st.button("戻る")
        if back_button:
            back_to_calendar()
        st.title(date.strftime("%Y/%m/%d"))
        icon = st.selectbox("感情", ["🥰", "😊", "😑", "😥", "😓"])
        content = st.text_area("内容")
        active_time = st.slider("活動時間", 4, 28, (7, 22))
        active_start = active_time[0]
        active_end = active_time[1]
        register_flag = False

        # 入力エラーを出力
        if st.button("登録"):
            if not icon:
                st.error("感情を選択してください")

            elif not content:
                st.error("内容を入力してください")

            elif active_start >= active_end:
                st.error("活動時間の開始時刻は終了時刻より前にしてください")

            else:
                register_flag = True

            if register_flag:
                add_diary_entry(conn, st.session_state["user_id"], date, icon, content, active_start, active_end)
                st.session_state["current_screen"] = "カレンダー"
                st.rerun()

    else:
        st.error("ログインしてください")
        st.session_state["current_screen"] = "ログイン"
        st.experimental_rerun()


def back_to_calendar():
    st.session_state["current_screen"] = "カレンダー"
    st.rerun()
