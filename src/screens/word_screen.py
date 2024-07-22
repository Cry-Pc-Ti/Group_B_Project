from wordcloud import WordCloud
import matplotlib.pyplot as plt
import streamlit as st
from janome.tokenizer import Tokenizer


def word_screen(c):

    st.title("ワードクラウド")

    st.header("2024/07/07-2024/07/13")

    columns =  st.columns([10,2,2])
    with columns[1]:
            st.button("前の週")
    with columns[2]:
            st.button("次の週")

    cur = c.cursor()
    cur.execute("SELECT content FROM contents")
    text = cur.fetchall()

    texts = "".join(map(str,text))
    tk = Tokenizer()
    tokens = tk.tokenize(texts)
    words=[]

    for token in tokens:
        token_list = token.part_of_speech.split(",")
        if token_list[0] == "名詞" and token_list[1] != "非自立":
            words.append(token.surface)
    words = " ".join(words)
    
    stopword = ["今日","朝","午後","夕方","夜","時間","週間","一"]
    wordcloud = WordCloud(font_path="static\\fonts\\NotoSansJP-Regular.ttf", background_color=None, mode='RGBA', width=480,height=250, stopwords=stopword).generate(words)

    plt.figure(figsize=(8,4), facecolor=(0,0,0,0))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    st.pyplot(plt)

    if st.button("back"):
        st.session_state["screen"] = "main"
        st.rerun()