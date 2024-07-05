import streamlit as st
import matplotlib.pyplot as plt
from events.diary_operations import get_diary_entries
from datetime import datetime, timedelta
import locale


def weekly_analysis_screen(conn):
    if "user_id" in st.session_state:
        user_id = st.session_state["user_id"]

        st.title("週間分析")

        # 選択された週の初めの日付
        start_of_week = st.session_state["start_of_week"]

        # 週を前後に移動するためのボタン
        col1, col2, col3 = st.columns([8, 1.5, 2])
        with col1:
            st.write("")
        with col2:
            if st.button("前の週"):
                st.session_state["start_of_week"] -= timedelta(days=7)
                st.rerun()
        with col3:
            if st.button("次の週"):
                st.session_state["start_of_week"] += timedelta(days=7)
                st.rerun()

        # 今週の各日付を取得
        locale.setlocale(locale.LC_TIME, "en_US.utf8")
        dates = [start_of_week + timedelta(days=i) for i in range(7)]
        format_dates = [date.strftime("%m/%d") + "\n(" + date.strftime("%a") + ")" for date in dates]

        # 日記エントリーを辞書型のリストとして取得
        diaries = get_diary_entries(conn, user_id)

        # 感情評価のためのマッピング
        icon_to_score = {"🥰": 5, "😊": 4, "😑": 3, "😥": 2, "😓": 1}

        # データの整形
        scores = []
        sleep_times = []

        for date in dates:
            diary = next((diary for diary in diaries if diary["date"].date() == date.date()), None)
            if diary:
                scores.append(icon_to_score[diary["icon"]])
                sleep_duration = diary["sleep_end"] - diary["sleep_start"]
                sleep_times.append(sleep_duration.total_seconds() / 3600.0)  # 時間に変換
            else:
                scores.append(0)
                sleep_times.append(0)

        # グラフの作成
        fig, ax1 = plt.subplots()

        # 睡眠時間の棒グラフ
        ax1_color = "#FF4B4B"
        ax1.set_ylabel("睡眠時間 (時間)", font="MS Gothic")
        ax1.bar(format_dates, sleep_times, color=ax1_color, alpha=0.4)
        ax1.tick_params(axis="y", labelcolor=ax1_color)
        ax1.set_ylim(0, 12)

        # 感情スコアのプロット
        ax2 = ax1.twinx()
        ax2_color = "#FF8700"
        ax2.set_ylabel("感情スコア", font="MS Gothic")
        ax2.plot(format_dates, scores, marker="o", color=ax2_color)
        ax2.tick_params(axis="y", labelcolor=ax2_color)
        ax2.set_ylim(0, 5)

        # グラフのタイトルとレイアウト
        plt.title("今週の感情スコアと睡眠時間", font="MS Gothic")
        fig.tight_layout()
        st.pyplot(fig)

    else:
        st.error("ログインしてください")
        st.session_state["current_screen"] = "ログイン"
        st.rerun()
