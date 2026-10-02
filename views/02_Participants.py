import streamlit as st


from src.analytics import (
    get_messages_per_user,
    get_user_statistics,
    get_words_per_user
)


st.set_page_config(
    page_title="Participants",
    page_icon="💬",
    layout="wide"
)


df = st.session_state.get("chat_df")

if df is None:
    st.warning("No chat loaded.")
    st.stop()


st.title("Participant Analysis")

st.caption(
    "Analyze participation patterns and individual activity."
)

st.divider()


# -----------------------------
# Participant Statistics
# -----------------------------

user_statistics = get_user_statistics(df)

st.subheader("Participant Statistics")

if not user_statistics.empty:

    display_statistics = (
        user_statistics
        .copy()
        .round(2)
    )

    st.dataframe(
        display_statistics,
        use_container_width=True
    )

else:

    st.info(
        "No participant statistics available."
    )


# -----------------------------
# Messages per Participant
# -----------------------------

st.divider()

st.subheader("Messages per Participant")

messages_per_user = get_messages_per_user(df)

if not messages_per_user.empty:
    st.bar_chart(messages_per_user)

else:
    st.info(
        "No message data available."
    )


# -----------------------------
# Words per Participant
# -----------------------------

st.divider()

st.subheader("Words per Participant")

words_per_user = get_words_per_user(df)

if not words_per_user.empty:
    st.bar_chart(words_per_user)

else:
    st.info(
        "No word data available."
    )


# -----------------------------
# Participant Detail
# -----------------------------

st.divider()

st.subheader("Participant Detail")

participants = sorted(
    df["sender"].dropna().unique()
)

selected_user = st.selectbox(
    "Select participant",
    ["All"] + participants
)


if selected_user != "All":

    user_data = df[
        df["sender"] == selected_user
    ]

    user_messages = len(user_data)

    user_words = int(
        user_data["word_count"].sum()
    )

    user_average_length = round(
        user_data["character_count"].mean(),
        2
    )

    user_media = int(
        user_data["is_media"].sum()
    )

    user_links = int(
        user_data["has_url"].sum()
    )


    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            "Messages",
            user_messages
        )

    with col2:
        st.metric(
            "Words",
            user_words
        )

    with col3:
        st.metric(
            "Avg Message Length",
            user_average_length
        )

    with col4:
        st.metric(
            "Media",
            user_media
        )

    with col5:
        st.metric(
            "Links",
            user_links
        )


    st.subheader(
        f"Activity: {selected_user}"
    )

    user_hourly = (
        user_data
        .groupby("hour")
        .size()
        .reindex(
            range(24),
            fill_value=0
        )
    )

    st.line_chart(user_hourly)