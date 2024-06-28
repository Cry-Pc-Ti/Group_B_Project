import streamlit as st
from screen.login_screen import login_page


def main():
    st.set_page_config(
        page_title="Streamlit App",
        page_icon="static/img/icon.png",
    )
    login_page()


if __name__ == "__main__":
    main()
