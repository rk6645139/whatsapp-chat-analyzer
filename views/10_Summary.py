import streamlit as st
import pandas as pd

from src.analytics import get_messages_per_user
from src.temporal import get_activity_summary
from src.nlp import get_word_frequency
from src.summary import (
    generate_conversation_summary,
    format_summary
)


st.set_page_config(
    page_title="Conversation Summary",
    page_icon="📋",
    layout="wide"
)


df = st.session_state.get("chat_df")


if df is None:
    st.warning("No chat loaded.")
    st.stop()


st.title("Conversation Summary")

st.caption(
    "A consolidated overview of the conversation "
    "using the available analytics."
)

st.divider()


# --------------------------------------------------
# Combine available analysis results
# --------------------------------------------------

analysis_df = df.copy()


sentiment_df = st.session_state.get(
    "sentiment_df"
)

if sentiment_df is not None:

    sentiment_columns = [
        "sentiment",
        "sentiment_score"
    ]

    available_columns = [
        column
        for column in sentiment_columns
        if column in sentiment_df.columns
    ]

    if available_columns:

        analysis_df = analysis_df.drop(
            columns=available_columns,
            errors="ignore"
        )

        analysis_df = analysis_df.join(
            sentiment_df[available_columns]
        )


toxicity_df = st.session_state.get(
    "toxicity_df"
)

if toxicity_df is not None:

    toxicity_columns = [
        "toxicity_label",
        "toxicity_score"
    ]

    available_columns = [
        column
        for column in toxicity_columns
        if column in toxicity_df.columns
    ]

    if available_columns:

        analysis_df = analysis_df.drop(
            columns=available_columns,
            errors="ignore"
        )

        analysis_df = analysis_df.join(
            toxicity_df[available_columns]
        )


# --------------------------------------------------
# Basic analytics
# --------------------------------------------------

messages_per_user = get_messages_per_user(
    analysis_df
)

activity_summary = get_activity_summary(
    analysis_df
)

word_frequency = get_word_frequency(
    analysis_df,
    top_n=10
)


# --------------------------------------------------
# Sentiment summary
# --------------------------------------------------

sentiment_percentage = None


if "sentiment" in analysis_df.columns:

    valid_sentiment = analysis_df[
        analysis_df["sentiment"]
        != "not_applicable"
    ]

    if not valid_sentiment.empty:

        sentiment_percentage = (
            valid_sentiment["sentiment"]
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

        sentiment_percentage = (
            sentiment_percentage
            / sentiment_percentage.sum()
            * 100
        ).round(2)


# --------------------------------------------------
# Toxicity summary
# --------------------------------------------------

toxicity_percentage = None


if "toxicity_label" in analysis_df.columns:

    valid_toxicity = analysis_df[
        analysis_df["toxicity_label"]
        != "not_applicable"
    ]

    if not valid_toxicity.empty:

        toxicity_percentage = (
            valid_toxicity["toxicity_label"]
            .value_counts()
            .reindex(
                [
                    "non-toxic",
                    "toxic"
                ],
                fill_value=0
            )
        )

        toxicity_percentage = (
            toxicity_percentage
            / toxicity_percentage.sum()
            * 100
        ).round(2)


# --------------------------------------------------
# Generate summary
# --------------------------------------------------

summary = generate_conversation_summary(
    df=analysis_df,
    messages_per_user=messages_per_user,
    activity_summary=activity_summary,
    word_frequency=word_frequency,
    sentiment_percentage=sentiment_percentage,
    toxicity_percentage=toxicity_percentage
)


summary_lines = format_summary(
    summary
)


# --------------------------------------------------
# Overview
# --------------------------------------------------

st.subheader("Conversation Overview")


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Messages",
        summary["total_messages"]
    )


with col2:

    st.metric(
        "Participants",
        summary["total_participants"]
    )


with col3:

    st.metric(
        "Most Active Day",
        summary["most_active_day"]
    )


with col4:

    st.metric(
        "Most Active Hour",
        f'{summary["most_active_hour"]}:00'
    )


# --------------------------------------------------
# Activity
# --------------------------------------------------

st.divider()

st.subheader("Activity Highlights")


for line in summary_lines:

    st.write(
        f"• {line}"
    )


# --------------------------------------------------
# Participant Activity
# --------------------------------------------------

st.divider()

st.subheader("Participant Activity")


participant_df = (
    messages_per_user
    .rename("messages")
    .to_frame()
)


st.bar_chart(
    participant_df
)


# --------------------------------------------------
# Top Words
# --------------------------------------------------

st.divider()

st.subheader("Most Frequent Words")


if word_frequency:

    word_df = pd.DataFrame(
        word_frequency,
        columns=[
            "word",
            "frequency"
        ]
    ).set_index("word")

    st.bar_chart(
        word_df
    )

else:

    st.info(
        "No word-frequency data available."
    )


# --------------------------------------------------
# Sentiment
# --------------------------------------------------

if sentiment_percentage is not None:

    st.divider()

    st.subheader(
        "Sentiment Overview"
    )

    sentiment_df_display = (
        sentiment_percentage
        .rename("percentage")
        .to_frame()
    )

    st.bar_chart(
        sentiment_df_display
    )

else:

    st.info(
        "Run Sentiment Analysis to include "
        "sentiment information in this summary."
    )


# --------------------------------------------------
# Toxicity
# --------------------------------------------------

if toxicity_percentage is not None:

    st.divider()

    st.subheader(
        "Toxicity Overview"
    )

    toxicity_df_display = (
        toxicity_percentage
        .rename("percentage")
        .to_frame()
    )

    st.bar_chart(
        toxicity_df_display
    )

else:

    st.info(
        "Run Toxicity Analysis to include "
        "toxicity information in this summary."
    )


# --------------------------------------------------
# Topic analysis status
# --------------------------------------------------

st.divider()

st.subheader("Advanced Analysis")


topic_results = st.session_state.get(
    "topic_results"
)

response_df = st.session_state.get(
    "response_df"
)


col1, col2 = st.columns(2)


with col1:

    if topic_results is not None:

        st.success(
            "Topic modeling completed."
        )

    else:

        st.info(
            "Topic modeling has not been run yet."
        )


with col2:

    if response_df is not None:

        st.success(
            "Response analysis completed."
        )

    else:

        st.info(
            "Response analysis has not been run yet."
        )


# --------------------------------------------------
# Export
# --------------------------------------------------

st.divider()

st.subheader("Export Summary")


summary_text = "\n".join(
    summary_lines
)


st.download_button(
    "Download Summary",
    data=summary_text,
    file_name="conversation_summary.txt",
    mime="text/plain"
)