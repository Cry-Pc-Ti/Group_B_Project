import streamlit as st
import matplotlib.pyplot as plt
from events.diary_operations import get_diary_entries
from datetime import datetime, timedelta
import matplotlib.dates as mdates


def weekly_analysis_screen(conn):
    if "user_id" in st.session_state:
        st.title("週間分析")

        # 日記エントリーを辞書型のリストとして取得
        diaries = get_diary_entries(conn, st.session_state["user_id"])

        # 今週の日記を取得
        today = datetime.now()
        start_of_week = today - timedelta(days=today.weekday())  # 週の初めの日付（月曜日）
        dates = [start_of_week + timedelta(days=i) for i in range(7)]  # 今週の各日付
        format_dates = [date.strftime("%m/%d") for date in dates]

        # 感情評価のためのマッピング
        icon_to_score = {"🥰": 5, "😊": 4, "😑": 3, "😥": 2, "😓": 1}

        # データの整形
        scores = []
        active_times = []

        for date in dates:
            diary = next((diary for diary in diaries if diary["date"].date() == date.date()), None)
            if diary:
                scores.append(icon_to_score[diary["icon"]])
                active_times.append(diary["active_end"] - diary["active_start"])
            else:
                scores.append(0)
                active_times.append(0)

        # グラフの作成
        fig, ax1 = plt.subplots()

        # 活動時間の棒グラフ
        ax1_color = "#3E16BD"
        ax1.set_ylabel("活動時間 (時間)", font="MS Gothic")
        ax1.bar(format_dates, active_times, color=ax1_color, alpha=0.4)
        ax1.tick_params(axis="y", labelcolor=ax1_color)

        # 感情スコアのプロット
        ax2 = ax1.twinx()
        ax2_color = "#0F75ED"
        ax2.set_ylabel("感情スコア", font="MS Gothic")
        ax2.plot(format_dates, scores, marker="o", color=ax2_color)
        ax2.tick_params(axis="y", labelcolor=ax2_color)
        ax2.set_ylim(0, 5)

        # グラフのタイトルとレイアウト
        plt.title("今週の感情スコアと活動時間", font="MS Gothic")
        fig.tight_layout()
        st.pyplot(fig)

    else:
        st.error("ログインしてください")
        st.session_state["current_screen"] = "ログイン"
        st.rerun()
