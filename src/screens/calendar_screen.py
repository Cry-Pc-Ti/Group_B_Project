import streamlit as st
from events.diary_operations import get_diary_entries, get_diary_by_date
import streamlit_calendar as st_calendar
from datetime import datetime, timedelta


def diary_calendar_screen(conn):
    if "user_id" in st.session_state:
        user_id = st.session_state["user_id"]

        # 日記エントリーを辞書型のリストとして取得
        diaries = get_diary_entries(conn, user_id)
        events = []

        for diary in diaries:
            events.append(
                {
                    "id": diary["id"],
                    "title": diary["icon"],
                    "start": diary["date"].strftime("%Y-%m-%dT%H:%M:%S"),
                    "allDay": True,
                    "color": "#00000000",
                    "backgroundColor": "#00000000",
                }
            )

        css = """
            <style>
                .fc {}
                .fc-direction-ltr {
                    text-align: center;
                }
                .fc-event-title-container {}
                .fc-event-title {
                    font-size: 45px;
                }
            </style>
            """

        # カレンダー表示
        st.title("カレンダー")
        selected_event = st_calendar.calendar(events=events, custom_css=css)

        # 日付がクリックされた場合
        if selected_event and selected_event["callback"] == "dateClick":
            date_str = selected_event["dateClick"]["date"]
            date = (datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ") + timedelta(days=1)).date()
            today = datetime.now().date()

            # 明日以降の日付は選択できないようにする
            if date > today:
                st.error("明日以降の日付は選択できません")
                st.stop()

            # DBにdateが一致するものがあるかを検索
            diary = get_diary_by_date(conn, user_id, date)
            if diary:
                # 日記が存在する場合、その日記を表示する画面に遷移
                st.session_state["current_screen"] = "日記詳細"
                st.session_state["selected_date"] = date
            else:
                # 日記が存在しない場合、新規登録画面に遷移
                st.session_state["current_screen"] = "日記登録"
                st.session_state["selected_date"] = date

        # イベントがクリックされた場合
        elif selected_event and selected_event["callback"] == "eventClick":
            date_str = selected_event["eventClick"]["event"]["start"]
            st.write(date_str)
            date = (datetime.strptime(date_str, "%Y-%m-%d")).date()
            diary = get_diary_by_date(conn, user_id, date)

            if diary:
                st.session_state["current_screen"] = "日記詳細"
                st.session_state["selected_date"] = date
            else:
                st.error("日記が存在しません")
                st.session_state["current_screen"] = "カレンダー"

            st.rerun()

    else:
        st.error("ログインしてください")
        st.session_state["current_screen"] = "ログイン"
        st.rerun()
