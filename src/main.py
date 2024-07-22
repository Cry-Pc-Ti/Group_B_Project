import streamlit as st
import sqlite3

from events.db import content_db, user_db
from screens.login_screen import login_screen
from screens.main_screen import main_screen
from screens.word_screen import word_screen

conn = sqlite3.connect("static/db/user.db")
user_db(conn)
c = sqlite3.connect("static/db/content.db")
content_db(c)


def main():
    if "screen" not in st.session_state:
        st.session_state["screen"] = "login"
    
    if st.session_state["screen"] == "login":
        login_screen(conn)
        
    if st.session_state["screen"] == "main":
        main_screen(c)
    
    elif st.session_state["screen"] == "word":
        word_screen(c)

if __name__ == "__main__":
    main()
