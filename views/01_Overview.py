import streamlit as st

from src.ui import render_sidebar

from src.analytics import (
    get_total_messages,
    get_participant_count,
    get_messages_per_user,
    get_media_count,
    get_link_count,
    get_total_url_count,
    get_average_message_length
)

from src.temporal import get_activity_summary


st.set_page_config(
    page_title="Overview",
    page_icon="💬",
    layout="wide"
)


df = render_sidebar()

if df is None:
    st.info("Upload a WhatsApp chat from the sidebar.")
    st.stop()


# -----------------------------
# Page Header
# -----------------------------

st.title("Overview")

st.caption(
    "High-level statistics and conversation activity."
)

st.divider()


# -----------------------------
# Core Statistics
# -----------------------------

total_messages = get_total_messages(df)

participant_count = get_participant_count(df)

messages_per_user = get_messages_per_user(df)

media_count = get_media_count(df)

link_count = get_link_count(df)

total_url_count = get_total_url_count(df)

average_message_length = get_average_message_length(df)

activity_summary = get_activity_summary(df)


# -----------------------------
# KPI Cards
# -----------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Messages",
        total_messages
    )

with col2:
    st.metric(
        "Participants",
        participant_count
    )

with col3:
    st.metric(
        "Media Messages",
        media_count
    )

with col4:
    st.metric(
        "Links Shared",
        total_url_count
    )


# -----------------------------
# Activity Overview
# -----------------------------

st.divider()

st.subheader("Activity Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Most Active Participant",
        messages_per_user.index[0]
        if not messages_per_user.empty
        else "N/A"
    )

with col2:
    st.metric(
        "Most Active Day",
        activity_summary["most_active_day"]
    )

with col3:
    st.metric(
        "Most Active Hour",
        f"{activity_summary['most_active_hour']}:00"
    )


# -----------------------------
# Participant Activity
# -----------------------------

st.divider()

st.subheader("Messages per Participant")

if not messages_per_user.empty:
    st.bar_chart(messages_per_user)
else:
    st.info("No participant activity available.")


# -----------------------------
# Conversation Statistics
# -----------------------------

st.divider()

st.subheader("Conversation Statistics")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Average Message Length",
        f"{average_message_length:.1f} characters"
    )

with col2:
    st.metric(
        "Messages Containing Links",
        link_count
    )

with col3:
    st.metric(
        "Active Hours",
        activity_summary["active_hours"]
    )