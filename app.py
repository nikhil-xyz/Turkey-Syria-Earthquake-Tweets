import streamlit as st
import pandas as pd
import pickle
import streamlit as st
import matplotlib.pyplot as plt
import helper
import seaborn as sns


df = pickle.load(open('tweets.pkl', 'rb'))

st.sidebar.image('cover.jpg')
st.sidebar.header("Turkey-Syria Earthquake Tweet's Analysis")

selected = st.sidebar.radio(
    'select an option',
    ('Overall', 'Language-Based Analysis', 'Source-Based Analysis')
)

language_tweets = df['language'].value_counts().head(20).reset_index()
language_tweets.rename(columns={'language': 'Tweet Count', 'index': 'Language'}, inplace=True)
source_tweets = df['source'].value_counts().head(30).reset_index()
source_tweets.rename(columns={'source': 'Tweet Count', 'index': 'Source'}, inplace=True)

if selected:
    if selected == 'Overall':
        st.header("Overall Analysis")

        df['isVerified'] = df['isVerified'].astype(int)
        pie_plot_verified = df['isVerified'].value_counts()
        pie_plot_verified.rename(index={0:'Unverified', 1:'Verified'}, inplace=True)
        labels = 'Unverified', 'Verified'
        st.subheader('Verified Handles')

        col1, col2 = st.columns(2)
        with col1:
            chart_data = pd.DataFrame(data=pie_plot_verified)
            st.bar_chart(chart_data)
        with col2:
            # st.write('User-Ratio')
            helper.plot_pie(pie_plot_verified, labels)

        st.subheader("# Trending Hash Tags")
        hash_for_word_cloud = df.sort_values(by='followers_count', ascending=False).head(200)[
            'hashtags'].reset_index()
        df_wc = helper.word_cloud(hash_for_word_cloud, 'hashtags')
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        tweets_per_day = df['day'].value_counts().reset_index()
        tweets_per_day.rename(columns={'index': 'date', 'day': 'tweets'}, inplace=True)

        st.subheader('Tweets Everyday')
        fig, (line_chart, freq_chart) = plt.subplots(figsize=(9, 6), ncols=2)
        g = sns.lineplot(x="date", y="tweets", data=tweets_per_day, ax=line_chart)
        g.set(xticks=list(range(6, 22)))
        sns.heatmap(tweets_per_day, annot=True, cmap="Reds_r",
                    linewidths=2, ax=freq_chart)
        st.pyplot(fig)

        st.subheader('Hashtag Trends Each Day (Heatmap)')
        helper.plot_heatmap()

        col3, col4 = st.columns(2)
        with col3:
            st.subheader('Most Used Languages')
            helper.plot_bar_chart(language_tweets.head(10))
        with col4:
            st.subheader('Most Used Sources')
            helper.plot_bar_chart(source_tweets.head(10))

    if selected == 'Language-Based Analysis':
        st.header("Language-Based Analysis")

        unique_lang = df['language'].value_counts().head(10).reset_index()
        option = st.sidebar.selectbox(
            'select the language',
            unique_lang['index']
        )

        st.subheader('Tweets per Language (Top 20)')
        helper.plot_bar_chart(language_tweets)

        lang_df = df[df['language'] == option]
        cnt_lang_df = lang_df['day'].value_counts().reset_index()
        cnt_lang_df.rename(columns={'index': 'date', 'day': 'freq'}, inplace=True)

        st.subheader('Tweets Everyday')
        st.write(option)
        fig, (line_chart, freq_chart) = plt.subplots(figsize=(9, 6), ncols=2)
        g = sns.lineplot(x="date", y="freq", data=cnt_lang_df, ax=line_chart)
        g.set(xticks=list(range(6, 22)))
        sns.heatmap(cnt_lang_df, annot=True, cmap="Blues",
                    linewidths=2, ax=freq_chart)
        st.pyplot(fig)

        verified_lang_users = lang_df['isVerified'].astype('int').value_counts()
        verified_lang_users.rename(index={0: 'Unverified', 1: 'Verified'}, inplace=True)
        verified_df_lang = pd.DataFrame(verified_lang_users)
        temp = verified_df_lang.rename(columns={'index':'Users', 'isVerified':'Tweets'})
        lang_users = temp.reset_index()
        labels = 'Unverified', 'Verified'
        st.subheader('Verified Handles')
        st.write(option)
        col5, col6 = st.columns(2)
        with col5:
            helper.plot_bar_chart(lang_users)
        with col6:
            # st.write('User-Ratio')
            helper.plot_pie(verified_lang_users, labels)

        st.subheader("Most Occured Words")
        hash_for_word_cloud = lang_df.sort_values(by='followers_count', ascending=False).head(200)[
            'content'].reset_index()
        df_wc = helper.word_cloud(hash_for_word_cloud, 'content')
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

    if selected == 'Source-Based Analysis':
        st.header("Source-Based Analysis")

        unique_source = df['source'].value_counts().head(10).reset_index()
        option = st.sidebar.selectbox(
            'select the language',
            unique_source['index']
        )

        st.subheader('Tweets per Source (Top 30)')
        helper.plot_bar_chart(source_tweets)

        source_df = df[df['source'] == option]
        cnt_src_df = source_df['day'].value_counts().reset_index()
        cnt_src_df.rename(columns={'index': 'date', 'day': 'freq'}, inplace=True)

        st.subheader('Tweets Everyday')
        st.write(option)
        fig, (line_chart, freq_chart) = plt.subplots(figsize=(9, 6), ncols=2)
        g = sns.lineplot(x="date", y="freq", data=cnt_src_df, ax=line_chart)
        g.set(xticks=list(range(6, 22)))
        sns.heatmap(cnt_src_df, annot=True, cmap="Blues",
                    linewidths=2, ax=freq_chart)
        st.pyplot(fig)

        verified_src_users = source_df['isVerified'].astype('int').value_counts()
        verified_src_users.rename(index={0: 'Unverified', 1: 'Verified'}, inplace=True)
        verified_df_src = pd.DataFrame(verified_src_users)
        temp = verified_df_src.rename(columns={'index': 'Users', 'isVerified': 'Tweets'})
        src_users = temp.reset_index()
        labels = 'Unverified', 'Verified'
        st.subheader('Verified Handles')
        st.write(option)
        col5, col6 = st.columns(2)
        with col5:
            helper.plot_bar_chart(src_users)
        with col6:
            # st.write('User-Ratio')
            helper.plot_pie(verified_src_users, labels)

        st.subheader("Most Occured Words")
        hash_for_word_cloud = source_df.sort_values(by='followers_count', ascending=False).head(200)[
            'content'].reset_index()
        df_wc = helper.word_cloud(hash_for_word_cloud, 'content')
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

