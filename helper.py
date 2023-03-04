import pandas as pd
import streamlit as st
import altair as alt
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import seaborn as sns
import pickle
import numpy as np
import cv2

def plot_bar_chart(tweet_df):
    x_name = tweet_df.columns[0]
    y_name = tweet_df.columns[1]
    st.write(alt.Chart(tweet_df).mark_bar().encode(
        x=alt.X(x_name, sort=None),
        y=y_name,
    ))

def plot_line_chart(tweet_df):
    x_name = tweet_df.columns[0]
    y_name = tweet_df.columns[1]
    st.write(alt.Chart(tweet_df).mark_line().encode(
        x=alt.X(x_name, sort=None),
        y=y_name,
    ))

def plot_pie(tweet_df, labels):
    explode = (0, 0.1)
    fig1, ax1 = plt.subplots()
    colors = ("orange", "brown")
    ax1.pie(tweet_df, explode=explode, colors=colors, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    st.pyplot(fig1)

def word_cloud(hashtags, col):
    mask = np.array(cv2.imread("twitter.png"))
    stopwords = STOPWORDS
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='black', stopwords=stopwords, mask=mask)
    if col == 'hashtags':
        df_wc = wc.generate(hashtags[col].str.cat(sep=","))
    else:
        text = str(hashtags[col].values)
        df_wc = wc.generate(text)
    return df_wc

def plot_heatmap():
    table = pickle.load(open('table.pkl', 'rb'))
    fig, ax = plt.subplots(figsize=(9, 6), ncols=1)

    sns.heatmap(table, cmap="Greens",
                linewidths=0.5, ax=ax)
    st.pyplot(fig)

    # day_df = pd.DataFrame(list(df.groupby('day')['hash_tags']))
    # day_df.columns = ['date', 'hashtags']

    # top_hashtags = pd.DataFrame()
    # day_hash_freq = pd.DataFrame()
    # for i in range(len(day_df)):
    #     hold = pd.DataFrame(np.hstack(day_df['hashtags'][i])).value_counts().head(15)
    #     v1 = hold.index
    #     v2 = hold.values
    #     v1 = [i[0] for i in v1]
    #     v1 = np.array(v1)
    #     day_hash_freq = day_hash_freq.append(pd.DataFrame({'date': day_df['date'][i], 'hashtag': v1, 'Frequency': v2}),
    #                                          ignore_index=True)
    #     top_hashtags = top_hashtags.append(pd.DataFrame({'hashtag': v1, 'Frequency': v2}), ignore_index=True)

    # top_hashtags = top_hashtags.sort_values(by='Frequency', ascending=False, ignore_index=True).head(30)
    # top_hashtags = pd.DataFrame(top_hashtags['hashtag'].unique())
    # top_hashtags.columns = ['hashtag']

    # day_hash_freq = day_hash_freq.merge(top_hashtags, on='hashtag').sort_values(by='date', ascending=True)
    # table = day_hash_freq.pivot_table(index='date', columns='hashtag', values='Frequency', aggfunc='sum').fillna(
    #     0).astype('int')