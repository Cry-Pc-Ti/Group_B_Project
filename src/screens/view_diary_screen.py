import streamlit as st
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


def view_diary_screen(conn, date):
    if "user_id" in st.session_state:
        back_button = st.button("戻る")
        if back_button:
            back_to_calendar()

        st.title(date.strftime("%Y/%m/%d"))
        diary = get_diary_by_date(conn, st.session_state["user_id"], date)
        if diary:
            emoji = ["🥰", "😊", "😑", "😥", "😓"]
            selected_emoji = emoji.index(diary["icon"])
            st.selectbox("感情", ["🥰", "😊", "😑", "😥", "😓"], index=selected_emoji)

            st.text_area("内容", value=diary["content"])

            st.slider("活動時間", 4, 28, (diary["active_start"], diary["active_end"]))

        else:
            st.error("この日の日記は存在しません")
    else:
        st.error("ログインしてください")
        st.session_state["current_screen"] = "ログイン"
        st.experimental_rerun()


def back_to_calendar():
    st.session_state["current_screen"] = "カレンダー"
    st.rerun()
