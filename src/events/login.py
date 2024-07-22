import sqlite3
import streamlit as st

def login(conn,id,password):
    cur = conn.cursor()

    cur.execute("SELECT id FROM users WHERE user=? AND password=?",(id,password))
    user = cur.fetchone()
    if user:
        st.session_state["user_id"] =user
        st.session_state["screen"] = "main"
        st.rerun()
    else:
        return None