import locale
import streamlit as st
from datetime import date, datetime, time, timedelta
from models.diary import Diary
from events.diary_operations import add_diary_entry, get_diary_by_date


def add_diary_screen(conn):
    if "user_id" in st.session_state:
        user_id: int = st.session_state["user_id"]
        selected_date: date = st.session_state["selected_date"]
        today = datetime.now().date()

        # 日記がすでに存在するかチェック
        existing_diary = get_diary_by_date(conn, user_id, selected_date)
        if existing_diary:
            st.session_state["current_screen"] = "日記詳細"
            st.rerun()

        # ボタンを配置
        col1, col2, col3 = st.columns([6, 1, 1])
        with col1:
            back_button = st.button("カレンダーに戻る")
            if back_button:
                back_to_calendar()
        with col2:
            if st.button("前の日"):
                st.session_state["selected_date"] -= timedelta(days=1)
                st.rerun()
        with col3:
            if selected_date < today:
                if st.button("次の日"):
                    st.session_state["selected_date"] += timedelta(days=1)
                    st.rerun()

        # 日記の内容を入力
        locale.setlocale(locale.LC_TIME, "en_US.utf8")
        format_date = f"{selected_date.strftime('%Y/%m/%d')} ({selected_date.strftime('%a')})"
        st.title(format_date)

        icon = st.selectbox("感情", ["🥰", "😊", "😑", "😥", "😓"])

        content = st.text_area("内容")

        col1, col2 = st.columns(2)
        with col1:
            selected_sleep_start = st.time_input("就寝", value=time(22, 0), step=timedelta(minutes=30))
        with col2:
            selected_sleep_end = st.time_input("起床", value=time(7, 0), step=timedelta(minutes=30))

        # 就寝時間を日時に変換
        sleep_start = datetime.combine(selected_date, selected_sleep_start)

        # 就寝時間が17:00以降23:30以前の場合は日付を前日にする
        if selected_sleep_start >= time(17, 0) and selected_sleep_start <= time(23, 30):
            sleep_start -= timedelta(days=1)

        # 起床時間を日時に変換
        sleep_end = datetime.combine(selected_date, selected_sleep_end)

        # 入力エラーを出力
        register_flag = False
        if st.button("登録"):
            # 感情アイコン未入力
            if not icon:
                st.error("感情を選択してください")
                register_flag = False

            # 内容未入力
            elif not content:
                st.error("内容を入力してください")
                register_flag = False

            # 就寝時間と起床時間が同じ場合はエラーを出力
            elif selected_sleep_start == selected_sleep_end:
                st.error("就寝時間と起床時間が同じです")
                register_flag = False

            # 就寝時間より起床時間が前の場合はエラーを出力
            elif sleep_start >= sleep_end:
                st.error("就寝時間は起床時間より前に設定してください")
                register_flag = False

            else:
                register_flag = True

            if register_flag:
                diary = Diary(
                    id=None,
                    user_id=user_id,
                    date=selected_date,
                    icon=icon,
                    content=content,
                    sleep_start=sleep_start,
                    sleep_end=sleep_end,
                    create_at=None,
                )

                add_diary_entry(conn, diary)
                st.session_state["current_screen"] = "カレンダー"
                st.rerun()

    else:
        st.error("ログインしてください")
        st.session_state["current_screen"] = "ログイン"
        st.rerun()


def back_to_calendar():
    st.session_state["current_screen"] = "カレンダー"
    st.rerun()
