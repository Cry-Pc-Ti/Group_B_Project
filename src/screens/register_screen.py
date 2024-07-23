import streamlit as st
from events.register import register

def register_screen(conn):
    
    col1,col2 = st.columns([7,1])
    with col1:
        st.title("Register")
    with col2:
        if st.button("Back"):
            st.session_state["screen"] = "login"
            st.rerun()

    id = st.text_input("id")
    password = st.text_input("password", type="password")

    if st.button("OK"):
        if not id:
            st.warning("Please input your id")
            st.stop()
        if not password:
            st.warning("Please input your password")
            st.stop()
        if register(conn,id,password):
            st.success("success!")
        else:
            st.error("error")
