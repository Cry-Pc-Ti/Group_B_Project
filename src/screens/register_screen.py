import streamlit as st
from events.register import register

def register_screen(conn):
    st.title("Register")
    
    id = st.text_input("id")
    password = st.text_input("password", type="password")

    if st.button("OK"):
        # user_id = register(conn, id, password)
        # if user_id:
        #     st.success("success!")
        # else:
        #     st.error("error")
        if not id:
            st.warning("Please input your id")
            st.stop()
        if not password:
            st.warning("Please input your password")
            st.stop()
        else:
            st.success("success!")

    if st.button("Back"):
        st.session_state["screen"] = "login"
        st.rerun()