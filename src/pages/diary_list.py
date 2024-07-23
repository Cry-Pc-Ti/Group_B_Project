import streamlit as st

st.title("日記一覧")

col1, col2 = st.columns(2)
with col1:
    st.date_input("開始日")
with col2:
    st.date_input("終了日")

with st.expander("😊 2024/07/10 Wed"):
        st.text_area("内容", "今日はオフィスでの作業が中心でした。タスクが山積みで少し大変でしたが、一つ一つ片付けていくうちに達成感を感じました。ランチタイムに同僚と新しいレストランに行って、美味しいパスタを楽しみました。夕方はジムに行って汗を流し、リフレッシュできました。")
        st.text_input("睡眠時間", "00:10 ~ 06:45")

with st.expander("😊 2024/07/11 Thu"):
        st.text_area("内容", "リモートワークの日でした。自宅での作業は集中できる一方で、少し孤独感も感じます。午後には同僚とビデオ会議をして進捗を確認しました。仕事が終わった後は、近所の公園を散歩して自然の中でリラックスしました。夜は読書をして静かな時間を楽しみました。")
        st.text_input("睡眠時間", "23:50 ~ 06:30")

with st.expander("🥰 2024/07/12 Fri"):
        st.text_area("内容", "今日は一週間の締めくくり。重要なプレゼンテーションがありましたが、無事に成功しました。チームメンバーと一緒に達成感を共有して、素敵な気分です。仕事の後は、同僚と一緒に飲みに行って、楽しい時間を過ごしました。週末が楽しみです。")
        st.text_input("睡眠時間", "00:00 ~ 07:00")