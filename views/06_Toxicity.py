import pandas as pd
import streamlit as st

from src.toxicity import (
    load_toxicity_model,
    analyze_toxicity,
    get_valid_toxicity_data,
    get_toxicity_distribution,
    get_toxicity_percentage,
    get_toxicity_by_user,
    get_toxic_messages
)


st.set_page_config(
    page_title="Toxicity Analysis",
    page_icon="🛡️",
    layout="wide"
)


df = st.session_state.get("chat_df")


if df is None:
    st.warning("No chat loaded.")
    st.stop()


@st.cache_resource
def get_cached_toxicity_model():
    return load_toxicity_model()


st.title("Toxicity Analysis")

st.caption(
    "Identify potentially toxic messages and analyze "
    "toxicity patterns across the conversation."
)

st.divider()


if "toxicity_df" not in st.session_state:
    st.session_state.toxicity_df = None


if st.button(
    "Run Toxicity Analysis",
    type="primary"
):

    with st.spinner(
        "Loading toxicity model and analyzing messages..."
    ):

        model = get_cached_toxicity_model()

        toxicity_df = analyze_toxicity(
            df,
            model=model
        )

        st.session_state.toxicity_df = toxicity_df


toxicity_df = st.session_state.toxicity_df


if toxicity_df is None:

    st.info(
        "Click 'Run Toxicity Analysis' "
        "to analyze the conversation."
    )

    st.stop()


valid_data = get_valid_toxicity_data(
    toxicity_df
)


if valid_data.empty:

    st.warning(
        "No valid text messages were available "
        "for toxicity analysis."
    )

    st.stop()


percentage = get_toxicity_percentage(
    toxicity_df
)


non_toxic_percentage = percentage.get(
    "non-toxic",
    0
)

toxic_percentage = percentage.get(
    "toxic",
    0
)


# Metrics

col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Analyzed Messages",
        len(valid_data)
    )


with col2:

    st.metric(
        "Non-Toxic",
        f"{non_toxic_percentage:.1f}%"
    )


with col3:

    st.metric(
        "Potentially Toxic",
        f"{toxic_percentage:.1f}%"
    )


st.divider()


# Distribution

st.subheader("Toxicity Distribution")


distribution = get_toxicity_distribution(
    toxicity_df
)


distribution_df = pd.DataFrame(
    {
        "classification": distribution.index,
        "messages": distribution.values
    }
).set_index("classification")


st.bar_chart(
    distribution_df
)


st.divider()


# Toxicity by participant

st.subheader("Toxicity by Participant")


user_toxicity = get_toxicity_by_user(
    toxicity_df
)


if not user_toxicity.empty:

    user_toxicity = user_toxicity.reindex(
        columns=[
            "non-toxic",
            "toxic"
        ],
        fill_value=0
    )

    st.bar_chart(
        user_toxicity
    )

else:

    st.info(
        "No participant toxicity data available."
    )


st.divider()


# Toxic messages

st.subheader("Potentially Toxic Messages")


toxic_messages = get_toxic_messages(
    toxicity_df
)


if toxic_messages.empty:

    st.success(
        "No messages crossed the toxicity threshold."
    )

else:

    st.dataframe(
        toxic_messages,
        use_container_width=True
    )


st.divider()


# Participant detail

st.subheader("Participant Toxicity Detail")


participants = sorted(
    valid_data["sender"]
    .dropna()
    .unique()
)


selected_user = st.selectbox(
    "Select participant",
    ["All"] + participants,
    key="toxicity_user"
)


if selected_user != "All":

    user_data = valid_data[
        valid_data["sender"] == selected_user
    ]


    user_distribution = (
        user_data["toxicity_label"]
        .value_counts()
        .reindex(
            [
                "non-toxic",
                "toxic"
            ],
            fill_value=0
        )
    )


    user_percentage = (
        user_distribution
        / user_distribution.sum()
        * 100
    ).round(2)


    col1, col2 = st.columns(2)


    with col1:

        st.metric(
            "Non-Toxic",
            f"{user_percentage['non-toxic']:.1f}%"
        )


    with col2:

        st.metric(
            "Potentially Toxic",
            f"{user_percentage['toxic']:.1f}%"
        )


    st.bar_chart(
        user_distribution
    )