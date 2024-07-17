import streamlit as st
import streamlit_calendar as st_calendar
from datetime import datetime, timedelta, date
from sqlite3 import Connection
from models.diary import Diary
from typing import Any, List, Dict
from events.diary_operations import get_diary_entries, get_diary_by_date


def diary_calendar_screen(conn: Connection):
    if "user_id" in st.session_state:
        user_id: int = st.session_state["user_id"]

        # 日記エントリーを辞書型のリストとして取得
        diaries: List[Diary] = get_diary_entries(conn, user_id)
        events: List[Dict[str, Any]] = []

        if diaries:
            for diary in diaries:
                events.append(
                    {
                        "id": diary.id,
                        "title": diary.icon,
                        "start": diary.date.strftime("%Y-%m-%dT%H:%M:%S"),
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
        selected_event: Dict[str, Any] = st_calendar.calendar(events=events, custom_css=css)

        # 日付がクリックされた場合
        if selected_event and selected_event["callback"] == "dateClick":
            clicked_date_str: str = selected_event["dateClick"]["date"]
            clicked_date: date = (
                datetime.strptime(clicked_date_str, "%Y-%m-%dT%H:%M:%S.%fZ") + timedelta(days=1)
            ).date()
            today = datetime.now().date()

            # 明日以降の日付は選択できないようにする
            if clicked_date > today:
                st.error("明日以降の日付は選択できません")
                st.stop()

            # DBにdateが一致するものがあるかを検索
            diary = get_diary_by_date(conn, user_id, clicked_date)
            if diary:
                # 日記が存在する場合、その日記を表示する画面に遷移
                st.session_state["current_screen"] = "日記詳細"
                st.session_state["selected_date"] = clicked_date
            else:
                # 日記が存在しない場合、新規登録画面に遷移
                st.session_state["current_screen"] = "日記登録"
                st.session_state["selected_date"] = clicked_date

        # イベントがクリックされた場合
        elif selected_event and selected_event["callback"] == "eventClick":
            clicked_date_str = selected_event["eventClick"]["event"]["start"]
            st.write(clicked_date_str)
            clicked_date = (datetime.strptime(clicked_date_str, "%Y-%m-%d")).date()
            diary = get_diary_by_date(conn, user_id, clicked_date)

            if diary:
                st.session_state["current_screen"] = "日記詳細"
                st.session_state["selected_date"] = clicked_date
            else:
                st.error("日記が存在しません")
                st.session_state["current_screen"] = "カレンダー"

            st.rerun()

    else:
        st.error("ログインしてください")
        st.session_state["current_screen"] = "ログイン"
        st.rerun()
