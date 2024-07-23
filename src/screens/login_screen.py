import streamlit as st

from events.login import login

def login_screen(conn):
    
    col1,col2 = st.columns([7,1])
    with col1:
        st.title("Login")
    with col2:
        if st.button("Register"):
            st.session_state["screen"] = "register"
            st.rerun()

    id = st.text_input("id")
    password = st.text_input("password", type="password")

    if st.button("Go"):
        user_id = login(conn, id, password)
        if user_id:
            st.rerun()
        else:
            st.error("error")
