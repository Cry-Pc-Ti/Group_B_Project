import streamlit as st
from PIL import Image

# グローバル変数を使用して、初回実行フラグを管理
if "INITIAL_RUN" not in globals():
    INITIAL_RUN = True
else:
    INITIAL_RUN = False

# 初回実行時のみ設定するコード
if INITIAL_RUN:
    st.set_page_config(page_title=":)iary", page_icon=Image.open("static/img/icon.png"), initial_sidebar_state="auto")
    INITIAL_RUN = False

from datetime import datetime, timedelta
from events.database import create_connection, create_user_tables, create_diary_tables
from screens.list_diary_screen import list_diary_screen
from screens.login_screen import login_screen
from screens.register_screen import register_screen
from screens.add_diary_screen import add_diary_screen
from screens.view_diary_screen import view_diary_screen
from screens.calendar_screen import diary_calendar_screen
from screens.weekly_analysis_screen import weekly_analysis_screen
from screens.wordcloud_screen import wordcloud_screen


# データベース接続とテーブル作成
user_conn = create_connection("user")
create_user_tables(user_conn)

diary_conn = create_connection("diary")
create_diary_tables(diary_conn)

# サイドバーのボタンスタイルの設定
st.markdown(
    """
        <style>
            div[data-testid="stSidebarContent"] button {
                background-color: transparent !important;
                border: none !important;
                color: inherit !important;
            }
            div[data-testid="stSidebarContent"] button:hover {
                color: #FF4B4B !important;
            }
        </style>
    """,
    unsafe_allow_html=True,
)


# ページナビゲーション
def run_app():

    # セッション状態の初期化
    if "current_screen" not in st.session_state:
        st.session_state["current_screen"] = "ログイン"

    if "selected_date" not in st.session_state:
        st.session_state["selected_date"] = datetime.now().date()

    if "start_of_week" not in st.session_state:
        today = datetime.now()
        st.session_state["start_of_week"] = today - timedelta(days=today.weekday() + 1)

    # ログイン画面以外でサイドバーを表示
    if "user_id" in st.session_state:
        button_labels = ["日記登録", "カレンダー", "日記一覧", "週間分析", "ワードクラウド", "ログアウト"]

        for label in button_labels:
            if st.sidebar.button(label):
                st.session_state["current_screen"] = label

                if label == "日記登録":
                    # 日記登録画面に遷移する際に日付を今日にリセット
                    st.session_state["selected_date"] = datetime.now().date()

                # 週間分析画面に遷移する際に週初めの日付を今週日曜日の日付にリセット
                elif label == "週間分析" or label == "ワードクラウド":
                    today = datetime.now()
                    st.session_state["start_of_week"] = (today - timedelta(days=today.weekday() + 1)).date()

    if st.session_state["current_screen"] == "ログイン":
        login_screen(user_conn)

    elif st.session_state["current_screen"] == "ユーザ登録":
        register_screen(user_conn)

    elif st.session_state["current_screen"] == "日記登録":
        add_diary_screen(diary_conn)

    elif st.session_state["current_screen"] == "カレンダー":
        diary_calendar_screen(diary_conn)

    elif st.session_state["current_screen"] == "日記詳細":
        view_diary_screen(diary_conn)

    elif st.session_state["current_screen"] == "日記一覧":
        list_diary_screen(diary_conn)

    elif st.session_state["current_screen"] == "週間分析":
        weekly_analysis_screen(diary_conn)

    elif st.session_state["current_screen"] == "ワードクラウド":
        wordcloud_screen(diary_conn)

    elif st.session_state["current_screen"] == "ログアウト":
        st.session_state.clear()
        st.session_state["current_screen"] = "ログイン"
        st.rerun()


if __name__ == "__main__":
    run_app()
