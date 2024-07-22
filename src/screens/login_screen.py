import streamlit as st

from events.login import login
from events.register import register

def login_screen(conn):
    st.title("Login")

    id = st.text_input("id")
    password = st.text_input("password", type="password")

    if st.button("Go"):
        user_id = login(conn, id, password)
        if user_id:
            st.success("success")
            st.rerun()
        else:
            st.error("error")

    if st.button("Register"):
        if register(conn, id, password):
            st.success("success")
        else:
            st.error("error")