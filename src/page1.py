import streamlit as st

def page1():
    st.title("What's your name?")
    
    def change_page():
        st.session_state["page_select"] = "page2"

    st.text_input("Name", key="name")
    st.button(label="Submit", on_click=change_page)


def page2():
    name = st.session_state["name"]
    st.title(f"Hello, {name}")

    color = st.color_picker("Pick A Color", "#00f900")
    st.write("The current color is", color)

    def back_page():
        st.session_state["page_select"] = "page1"
    
    st.button(label="Back", on_click=back_page)


pages = dict(
    page1="ページ1",
    page2="ページ2",
)

page_id = st.sidebar.selectbox(
    "ページ名",
    ["page1", "page2"],
    format_func=lambda page_id: pages[page_id], # 描画する項目を日本語に変換
    key = "page_select",
)

if page_id == "page1":
    page1()

if page_id == "page2":
    page2()