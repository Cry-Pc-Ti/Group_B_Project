import streamlit as st
from sqlite3 import Connection
from events.diary_operations import get_diary_entries


def list_diary_screen(conn: Connection):

    if "user_id" in st.session_state:
        user_id: int = st.session_state["user_id"]
        diaries = get_diary_entries(conn, user_id)

        st.title("日記一覧")

        # 検索ボックスを追加
        search_term = st.text_input("検索", value="", placeholder="キーワードを入力してください")

        if not diaries:
            st.write("日記がありません。")
        else:
            # 降順にソート
            diaries = sorted(diaries, key=lambda x: x.date, reverse=True)

            # 検索キーワードでフィルタリング
            filtered_diaries = [diary for diary in diaries if search_term.lower() in diary.content.lower()]

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
