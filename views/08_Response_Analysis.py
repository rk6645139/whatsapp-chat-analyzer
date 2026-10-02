import pandas as pd
import streamlit as st

from src.response_analysis import (
    calculate_response_times,
    get_average_response_time,
    get_median_response_time,
    get_fastest_response,
    get_slowest_response,
    get_response_time_by_user,
    get_response_matrix
)


st.set_page_config(
    page_title="Response Analysis",
    page_icon="⏱️",
    layout="wide"
)


df = st.session_state.get("chat_df")


if df is None:
    st.warning("No chat loaded.")
    st.stop()


st.title("Response Analysis")

st.caption(
    "Analyze conversational response patterns "
    "and response times between participants."
)

st.divider()


# Configuration

st.subheader("Analysis Configuration")


max_gap = st.slider(
    "Maximum response gap (minutes)",
    min_value=5,
    max_value=180,
    value=60,
    step=5
)


st.caption(
    "Messages separated by more than this interval "
    "are treated as separate conversation activity "
    "rather than an immediate response."
)


if st.button(
    "Analyze Response Patterns",
    type="primary"
):

    with st.spinner(
        "Calculating response patterns..."
    ):

        response_df = calculate_response_times(
            df,
            max_gap_minutes=max_gap
        )

        st.session_state.response_df = response_df


response_df = st.session_state.get(
    "response_df"
)


if response_df is None:

    st.info(
        "Configure the response gap and click "
        "'Analyze Response Patterns'."
    )

    st.stop()


if response_df.empty:

    st.warning(
        "No response patterns could be identified "
        "with the selected time window."
    )

    st.stop()


# Metrics

st.subheader("Response Overview")


average_response = get_average_response_time(
    response_df
)

median_response = get_median_response_time(
    response_df
)

fastest_response = get_fastest_response(
    response_df
)

slowest_response = get_slowest_response(
    response_df
)


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Responses Analyzed",
        len(response_df)
    )


with col2:

    st.metric(
        "Average Response",
        f"{average_response:.2f} min"
    )


with col3:

    st.metric(
        "Median Response",
        f"{median_response:.2f} min"
    )


with col4:

    st.metric(
        "Fastest Response",
        f"{fastest_response:.2f} min"
    )


st.divider()


# Response distribution

st.subheader("Response Time Distribution")


response_distribution = pd.DataFrame(
    {
        "response_time": response_df[
            "response_time_minutes"
        ]
    }
)


st.bar_chart(
    response_distribution
)


# Response time by participant

st.divider()

st.subheader(
    "Response Time by Participant"
)


user_response = get_response_time_by_user(
    response_df
)


if not user_response.empty:

    display_response = user_response.copy()

    display_response[
        "average_response_time"
    ] = display_response[
        "average_response_time"
    ].round(2)

    display_response[
        "median_response_time"
    ] = display_response[
        "median_response_time"
    ].round(2)

    display_response[
        "fastest_response"
    ] = display_response[
        "fastest_response"
    ].round(2)

    display_response[
        "slowest_response"
    ] = display_response[
        "slowest_response"
    ].round(2)

    st.dataframe(
        display_response,
        use_container_width=True
    )

else:

    st.info(
        "No participant response data available."
    )


# User comparison

st.divider()

st.subheader(
    "Average Response Time"
)


if not user_response.empty:

    chart_data = user_response[
        ["average_response_time"]
    ].copy()

    chart_data.columns = [
        "Average Response (minutes)"
    ]

    st.bar_chart(
        chart_data
    )


# Response matrix

st.divider()

st.subheader(
    "Response Interaction Matrix"
)


response_matrix = get_response_matrix(
    response_df
)


if not response_matrix.empty:

    st.dataframe(
        response_matrix,
        use_container_width=True
    )

else:

    st.info(
        "No interaction matrix available."
    )


# Detailed responses

st.divider()

st.subheader(
    "Response Details"
)


display_columns = [
    "from_user",
    "to_user",
    "previous_message",
    "response_message",
    "response_time_minutes"
]


available_columns = [
    column
    for column in display_columns
    if column in response_df.columns
]


details = response_df[
    available_columns
].copy()


details[
    "response_time_minutes"
] = details[
    "response_time_minutes"
].round(2)


st.dataframe(
    details,
    use_container_width=True
)