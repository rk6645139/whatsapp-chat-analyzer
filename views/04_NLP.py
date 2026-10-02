import pandas as pd
import streamlit as st
from wordcloud import WordCloud

from src.nlp import (
    get_word_frequency,
    get_unique_word_count,
    get_emoji_frequency,
    get_total_emoji_count,
    get_average_words_per_message,
    get_longest_messages
)


st.set_page_config(
    page_title="NLP Analysis",
    page_icon="💬",
    layout="wide"
)

df = st.session_state.get("chat_df")

if df is None:
    st.warning("No chat loaded.")
    st.stop()

st.title("NLP Analysis")

st.caption(
    "Explore word usage, emojis and text characteristics "
    "across the conversation."
)

st.divider()


# -----------------------------
# NLP Metrics
# -----------------------------

total_unique_words = get_unique_word_count(df)

average_words = get_average_words_per_message(df)

total_emojis = get_total_emoji_count(df)


col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Unique Words",
        total_unique_words
    )

with col2:
    st.metric(
        "Avg Words / Message",
        round(average_words, 2)
    )

with col3:
    st.metric(
        "Total Emojis",
        total_emojis
    )


# -----------------------------
# Word Frequency
# -----------------------------

st.divider()

st.subheader("Most Frequent Words")

word_frequency = get_word_frequency(
    df,
    top_n=20
)

if word_frequency:

    word_df = pd.DataFrame(
        word_frequency,
        columns=[
            "word",
            "frequency"
        ]
    ).set_index("word")

    st.bar_chart(word_df)

else:

    st.info(
        "No word frequency data available."
    )


# -----------------------------
# WordCloud
# -----------------------------

st.divider()

st.subheader("WordCloud")

if word_frequency:

    word_counts = dict(
        word_frequency
    )

    wordcloud = WordCloud(
        width=1400,
        height=500,
        background_color="white",
        max_words=100,
        collocations=False
    ).generate_from_frequencies(
        word_counts
    )

    st.image(
        wordcloud.to_array(),
        use_container_width=True
    )

else:

    st.info(
        "Not enough text to generate a WordCloud."
    )


# -----------------------------
# Emoji Analysis
# -----------------------------

st.divider()

st.subheader("Most Used Emojis")

emoji_frequency = get_emoji_frequency(
    df,
    top_n=20
)

if emoji_frequency:

    emoji_df = pd.DataFrame(
        emoji_frequency,
        columns=[
            "emoji",
            "frequency"
        ]
    ).set_index("emoji")

    st.bar_chart(emoji_df)

else:

    st.info(
        "No emojis found in this conversation."
    )


# -----------------------------
# Longest Messages
# -----------------------------

st.divider()

st.subheader("Longest Messages")

longest_messages = get_longest_messages(
    df,
    top_n=10
)

if not longest_messages.empty:

    st.dataframe(
        longest_messages,
        use_container_width=True
    )

else:

    st.info(
        "No messages available."
    )


# -----------------------------
# Participant NLP
# -----------------------------

st.divider()

st.subheader("Participant NLP Analysis")

nlp_user = st.selectbox(
    "Select participant",
    ["All"] + sorted(df["sender"].unique()),
    key="nlp_user"
)

if nlp_user == "All":

    nlp_data = df

else:

    nlp_data = df[
        df["sender"] == nlp_user
    ]


user_word_frequency = get_word_frequency(
    nlp_data,
    top_n=15
)

if user_word_frequency:

    user_word_df = pd.DataFrame(
        user_word_frequency,
        columns=[
            "word",
            "frequency"
        ]
    ).set_index("word")

    st.bar_chart(user_word_df)

else:

    st.info(
        "No NLP data available for this participant."
    )