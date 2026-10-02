import streamlit as st

from src.ui import render_sidebar

from src.temporal import (
    get_daily_activity,
    get_weekly_activity,
    get_monthly_activity,
    get_hourly_activity,
    get_day_of_week_activity,
    get_activity_heatmap
)


st.set_page_config(
    page_title="Activity",
    page_icon="💬",
    layout="wide"
)


df = st.session_state.get("chat_df")

if df is None:
    st.warning("No chat loaded.")
    st.stop()


st.title("Activity Analysis")

st.caption(
    "Explore when the conversation is most active."
)

st.divider()


# -----------------------------
# Daily Activity
# -----------------------------

st.subheader("Daily Message Activity")

daily_activity = get_daily_activity(df)

if not daily_activity.empty:

    daily_activity = daily_activity.set_index(
        "date"
    )

    st.line_chart(
        daily_activity["messages"]
    )


# -----------------------------
# Hourly Activity
# -----------------------------

st.divider()

st.subheader("Messages by Hour")

hourly_activity = get_hourly_activity(df)

st.bar_chart(
    hourly_activity.set_index("hour")
)


# -----------------------------
# Day of Week
# -----------------------------

st.divider()

st.subheader("Messages by Day of Week")

weekday_activity = get_day_of_week_activity(df)

st.bar_chart(
    weekday_activity.set_index(
        "day_of_week"
    )
)


# -----------------------------
# Weekly Activity
# -----------------------------

st.divider()

st.subheader("Weekly Activity")

weekly_activity = get_weekly_activity(df)

if not weekly_activity.empty:

    weekly_activity = weekly_activity.set_index(
        "datetime"
    )

    st.line_chart(
        weekly_activity["messages"]
    )


# -----------------------------
# Monthly Activity
# -----------------------------

st.divider()

st.subheader("Monthly Activity")

monthly_activity = get_monthly_activity(df)

if not monthly_activity.empty:

    monthly_activity = monthly_activity.set_index(
        "datetime"
    )

    st.line_chart(
        monthly_activity["messages"]
    )


# -----------------------------
# Heatmap
# -----------------------------

st.divider()

st.subheader("Activity Heatmap")

heatmap = get_activity_heatmap(df)

st.dataframe(
    heatmap,
    use_container_width=True
)