import sqlite3
import streamlit as st

def register(conn,id,password):
    cur = conn.cursor()
    
    cur.execute("INSERT INTO users (user, password) VALUES(?,?)",(id,password))
    new = cur.fetchone()

    cur.execute("SELECT id FROM users WHERE user=? AND password=?",(id,password))
    user = cur.fetchone()

    try:
        if new == user:
            st.error("error")
        elif new:
            conn.commit()
            return True
    except sqlite3.IntegrityError:
        return False