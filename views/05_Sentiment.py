import pandas as pd
import streamlit as st

from src.sentiment import (
    load_sentiment_model,
    analyze_sentiment,
    get_sentiment_distribution,
    get_sentiment_percentage,
    get_sentiment_by_user,
    get_sentiment_over_time,
    get_valid_sentiment_data
)


st.set_page_config(
    page_title="Sentiment Analysis",
    page_icon="💬",
    layout="wide"
)


# --------------------------------
# Get processed chat
# --------------------------------

df = st.session_state.get(
    "chat_df"
)

if df is None:

    st.warning(
        "No chat loaded."
    )

    st.stop()


# --------------------------------
# Cached Model
# --------------------------------

@st.cache_resource
def get_cached_sentiment_model():

    return load_sentiment_model()


# --------------------------------
# Header
# --------------------------------

st.title("Sentiment Analysis")

st.caption(
    "Analyze positive, neutral and negative sentiment "
    "across the conversation."
)

st.divider()


# --------------------------------
# Run Analysis
# --------------------------------

if "sentiment_df" not in st.session_state:

    st.session_state.sentiment_df = None


if st.button(
    "Run Sentiment Analysis",
    type="primary"
):

    with st.spinner(
        "Loading sentiment model and analyzing messages..."
    ):

        model = (
            get_cached_sentiment_model()
        )

        sentiment_df = analyze_sentiment(
            df,
            model=model
        )

        st.session_state.sentiment_df = (
            sentiment_df
        )


# --------------------------------
# Check Results
# --------------------------------

sentiment_df = (
    st.session_state.sentiment_df
)


if sentiment_df is None:

    st.info(
        "Click 'Run Sentiment Analysis' "
        "to analyze the conversation."
    )

    st.stop()


# --------------------------------
# Valid Results
# --------------------------------

valid_data = (
    get_valid_sentiment_data(
        sentiment_df
    )
)


if valid_data.empty:

    st.warning(
        "No valid text messages were available "
        "for sentiment analysis."
    )

    st.stop()


# --------------------------------
# Sentiment Percentages
# --------------------------------

percentage = (
    get_sentiment_percentage(
        sentiment_df
    )
)


positive_percentage = percentage.get(
    "positive",
    0
)

neutral_percentage = percentage.get(
    "neutral",
    0
)

negative_percentage = percentage.get(
    "negative",
    0
)


# --------------------------------
# KPI Cards
# --------------------------------

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Analyzed Messages",
        len(valid_data)
    )


with col2:

    st.metric(
        "Positive",
        f"{positive_percentage:.1f}%"
    )


with col3:

    st.metric(
        "Neutral",
        f"{neutral_percentage:.1f}%"
    )


with col4:

    st.metric(
        "Negative",
        f"{negative_percentage:.1f}%"
    )


# --------------------------------
# Distribution
# --------------------------------

st.divider()

st.subheader(
    "Sentiment Distribution"
)


distribution = (
    get_sentiment_distribution(
        sentiment_df
    )
)


distribution_df = pd.DataFrame(
    {
        "sentiment": distribution.index,
        "messages": distribution.values
    }
).set_index(
    "sentiment"
)


st.bar_chart(
    distribution_df
)


# --------------------------------
# Sentiment by Participant
# --------------------------------

st.divider()

st.subheader(
    "Sentiment by Participant"
)


user_sentiment = (
    get_sentiment_by_user(
        sentiment_df
    )
)


if not user_sentiment.empty:

    user_sentiment = (
        user_sentiment
        .reindex(
            columns=[
                "positive",
                "neutral",
                "negative"
            ],
            fill_value=0
        )
    )

    st.bar_chart(
        user_sentiment
    )

else:

    st.info(
        "No participant sentiment data available."
    )


# --------------------------------
# Sentiment Over Time
# --------------------------------

st.divider()

st.subheader(
    "Sentiment Over Time"
)


sentiment_time = (
    get_sentiment_over_time(
        sentiment_df
    )
)


if not sentiment_time.empty:

    sentiment_time = (
        sentiment_time
        .pivot(
            index="date",
            columns="sentiment",
            values="messages"
        )
        .fillna(0)
    )

    st.line_chart(
        sentiment_time
    )

else:

    st.info(
        "No time-based sentiment data available."
    )


# --------------------------------
# Strongest Sentiment Messages
# --------------------------------

st.divider()

st.subheader(
    "High-Confidence Sentiment Predictions"
)


confidence_data = valid_data[
    [
        "datetime",
        "sender",
        "message",
        "sentiment",
        "sentiment_score"
    ]
].copy()


confidence_data = (
    confidence_data
    .sort_values(
        "sentiment_score",
        ascending=False
    )
    .head(20)
)


st.dataframe(
    confidence_data,
    use_container_width=True
)


# --------------------------------
# Participant Detail
# --------------------------------

st.divider()

st.subheader(
    "Participant Sentiment Detail"
)


participants = sorted(
    valid_data["sender"]
    .dropna()
    .unique()
)


selected_user = st.selectbox(
    "Select participant",
    ["All"] + participants,
    key="sentiment_user"
)


if selected_user != "All":

    user_data = valid_data[
        valid_data["sender"]
        == selected_user
    ]


    user_distribution = (
        user_data["sentiment"]
        .value_counts()
        .reindex(
            [
                "positive",
                "neutral",
                "negative"
            ],
            fill_value=0
        )
    )


    user_percentage = (
        user_distribution
        / user_distribution.sum()
        * 100
    ).round(2)


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "Positive",
            f"{user_percentage['positive']:.1f}%"
        )


    with col2:

        st.metric(
            "Neutral",
            f"{user_percentage['neutral']:.1f}%"
        )


    with col3:

        st.metric(
            "Negative",
            f"{user_percentage['negative']:.1f}%"
        )


    st.bar_chart(
        user_distribution
    )