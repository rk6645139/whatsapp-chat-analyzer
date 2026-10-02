import streamlit as st
import pandas as pd

from src.search import (
    search_messages,
    format_search_results
)


st.set_page_config(
    page_title="Message Search",
    page_icon="🔎",
    layout="wide"
)


df = st.session_state.get("chat_df")


if df is None:

    st.warning("No chat loaded.")
    st.stop()


st.title("Message Explorer")

st.caption(
    "Search and filter messages across the entire conversation."
)

st.divider()


# Search controls

st.subheader("Search Filters")


query = st.text_input(
    "Search messages",
    placeholder="Enter a keyword or phrase..."
)


participants = sorted(
    df["sender"]
    .dropna()
    .unique()
)


selected_user = st.selectbox(
    "Participant",
    ["All"] + participants
)


col1, col2 = st.columns(2)


with col1:

    valid_dates = df["datetime"].dropna()

    if valid_dates.empty:
        st.warning("No valid dates were found in the uploaded chat.")
        st.stop()

    min_date = valid_dates.min().date()
    max_date = valid_dates.max().date()

    start_date = st.date_input(
        "Start date",
        value=min_date,
        min_value=min_date,
        max_value=max_date
    )


with col2:

    end_date = st.date_input(
        "End date",
        value=max_date,
        min_value=min_date,
        max_value=max_date
    )


col1, col2 = st.columns(2)


with col1:

    sentiment_options = ["All"]

    if "sentiment" in df.columns:

        sentiment_options += sorted(
            df["sentiment"]
            .dropna()
            .unique()
            .tolist()
        )

    selected_sentiment = st.selectbox(
        "Sentiment",
        sentiment_options
    )


with col2:

    toxicity_options = ["All"]

    if "toxicity_label" in df.columns:

        toxicity_options += sorted(
            df["toxicity_label"]
            .dropna()
            .unique()
            .tolist()
        )

    selected_toxicity = st.selectbox(
        "Toxicity",
        toxicity_options
    )


col1, col2 = st.columns(2)


with col1:

    include_media = st.checkbox(
        "Include media messages",
        value=True
    )


with col2:

    include_deleted = st.checkbox(
        "Include deleted messages",
        value=False
    )


st.divider()


# Search

results = search_messages(
    df,
    query=query,
    user=selected_user,
    start_date=start_date,
    end_date=end_date,
    sentiment=selected_sentiment,
    toxicity=selected_toxicity,
    include_media=include_media,
    include_deleted=include_deleted
)


# Results summary

st.subheader("Search Results")


col1, col2 = st.columns(2)


with col1:

    st.metric(
        "Matching Messages",
        len(results)
    )


with col2:

    st.metric(
        "Search Scope",
        len(df)
    )


if results.empty:

    st.info(
        "No messages match the selected filters."
    )

    st.stop()


# Display results

display_results = format_search_results(
    results
)


st.dataframe(
    display_results,
    use_container_width=True,
    hide_index=True
)


# Export

st.divider()

st.subheader("Export Results")


csv_data = display_results.to_csv(
    index=False
).encode("utf-8")


st.download_button(
    label="Download Search Results",
    data=csv_data,
    file_name="whatsapp_search_results.csv",
    mime="text/csv"
)