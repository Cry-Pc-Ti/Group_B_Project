import matplotlib.pyplot as plt
from janome.tokenizer import Tokenizer
from wordcloud import WordCloud


def load_stopwords():
    with open("static/data/noun_stopwords.txt", "r", encoding="utf-8") as file:
        noun_stopwords = file.read().split(",")
    return set(noun_stopwords)


def generate_wordcloud(weekly_content: str):
    word_list = []

    tokenizer = Tokenizer()

    symbol_settings = list(tokenizer.sys_dic.unknowns["SYMBOL"][0])
    symbol_settings[3] = "記号,一般,*,*"
    tokenizer.sys_dic.unknowns["SYMBOL"][0] = symbol_settings

    for tokenizer in tokenizer.tokenize(weekly_content):
        word_type: str = tokenizer.part_of_speech.split(",")[0]
        test = tokenizer.part_of_speech.split(",")[1]
        is_number = tokenizer.part_of_speech.split(",")[1] == "数"
        if word_type in "名詞" and not is_number:
            word: str = tokenizer.surface
            print(word_type, test, word)
            word_list.append(word)

    # 抽出した名詞を空白区切りで連結
    word_chain = " ".join(word_list)

    if not word_chain:
        return None

    # 解析禁止ワードの読み込み
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
