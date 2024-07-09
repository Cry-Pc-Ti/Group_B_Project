import streamlit as st
from wordcloud import WordCloud
from janome.tokenizer import Tokenizer
import matplotlib.pyplot as plt


def load_stopwords():
    with open("static/data/noun_stopwords.txt", "r", encoding="utf-8") as file:
        noun_stopwords = file.read().split(",")
    return set(noun_stopwords)


def generate_wordcloud(weekly_content: str):
    if not weekly_content:
        st.warning("今週の日記がありません")
        return

    word_list = []

    token = Tokenizer()
    for token in token.tokenize(weekly_content):
        word_type = token.part_of_speech.split(",")[0]
        if word_type in "名詞":
            word_list.append(token.surface)

    word_chain = " ".join(word_list)

    noun_stopwords = load_stopwords()

    # ワードクラウドの作成
    font_path = "C:\Windows\Fonts\meiryo.ttc"
    wordcloud = WordCloud(
        stopwords=noun_stopwords,
        font_path=font_path,
        width=800,
        height=400,
        background_color="white",
    ).generate(word_chain)

    # プロット
    plt.figure(figsize=(8, 4))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")

    return plt
