import streamlit as st

from events.login import login

def login_screen(conn):
    st.title("Login")

    id = st.text_input("id")
    password = st.text_input("password", type="password")

    if st.button("Go"):
        user_id = login(conn, id, password)
        if user_id:
            st.rerun()
        else:
            st.error("error")

    if st.button("Register"):
        st.session_state["screen"] = "register"
        st.rerun()