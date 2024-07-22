import datetime
import streamlit as st
from sqlite3 import Connection
from events.diary_operations import get_diary_entries


def list_diary_screen(conn: Connection):
    if "user_id" in st.session_state:
        user_id: int = st.session_state["user_id"]
        diaries = get_diary_entries(conn, user_id)

        # 降順にソート
        diaries = sorted(diaries, key=lambda x: x.date, reverse=True)

        st.title("日記一覧")

        # 検索ボックス
        search_term = st.text_input("検索", value="", placeholder="キーワードを入力してください")

        # 日付絞り込み
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            if "start_date" not in st.session_state:
                st.session_state["start_date"] = datetime.date.today() - datetime.timedelta(days=30)
            start_date = st.date_input("開始日", value=st.session_state["start_date"])

        with col2:
            if "end_date" not in st.session_state:
                st.session_state["end_date"] = datetime.date.today()
            end_date = st.date_input("終了日", value=st.session_state["end_date"])

        with col3:
            st.write("")
            st.write("")
            if st.button("クリア"):
                st.session_state["start_date"] = None
                st.session_state["end_date"] = None
                st.experimental_rerun()

        if not diaries:
            st.write("日記がありません。")
        else:
            # 降順にソート
            diaries = sorted(diaries, key=lambda x: x.date, reverse=True)

            # 検索キーワードでフィルタリング
            filtered_diaries = [
                diary
                for diary in diaries
                if search_term.lower() in diary.content.lower()
                and (st.session_state["start_date"] is None or start_date <= diary.date)
                and (st.session_state["end_date"] is None or diary.date <= end_date)
            ]

            if not filtered_diaries:
                st.write("検索結果がありません。")
            else:
                for diary in filtered_diaries:
                    with st.expander(
                        f"{diary.icon}&emsp;**{diary.date.strftime('%Y/%m/%d')} ({diary.date.strftime('%a')})**"
                    ):
                        st.text_area(
                            label="**内容**",
                            value=diary.content,
                            key=f"content_{diary.id}",
                        )
                        st.text_input(
                            label="**睡眠時間**",
                            value=f"{diary.sleep_start.strftime('%H:%M')} ~ {diary.sleep_end.strftime('%H:%M')}",
                            key=f"sleep_time_{diary.id}",
                        )

    else:
        st.error("ログインしてください")
        st.session_state["current_screen"] = "ログイン"
        st.experimental_rerun()
