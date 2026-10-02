import pandas as pd
import streamlit as st

from src.topics import (
    prepare_topic_text,
    create_tfidf_matrix,
    perform_kmeans,
    get_cluster_keywords,
    calculate_silhouette_score,
    get_cluster_distribution
)


st.set_page_config(
    page_title="Topic Analysis",
    page_icon="📊",
    layout="wide"
)


df = st.session_state.get("chat_df")


if df is None:
    st.warning("No chat loaded.")
    st.stop()


st.title("Topic Analysis")

st.caption(
    "Discover recurring conversation themes using "
    "TF-IDF and KMeans clustering."
)

st.divider()


# Prepare text

topic_text = prepare_topic_text(df)


if len(topic_text) < 10:

    st.warning(
        "Not enough text messages are available "
        "for topic analysis."
    )

    st.stop()


st.subheader("Topic Model Configuration")


col1, col2 = st.columns(2)


with col1:

    max_clusters = min(
        8,
        max(2, len(topic_text) // 5)
    )

    n_clusters = st.slider(
        "Number of Topics",
        min_value=2,
        max_value=max_clusters,
        value=min(5, max_clusters)
    )


with col2:

    top_keywords = st.slider(
        "Keywords per Topic",
        min_value=5,
        max_value=15,
        value=10
    )


st.caption(
    "The number of topics controls how many conversation "
    "clusters the model will discover."
)


if st.button(
    "Discover Topics",
    type="primary"
):

    with st.spinner(
        "Building TF-IDF matrix and discovering topics..."
    ):

        try:

            vectorizer, matrix = (
                create_tfidf_matrix(
                    topic_text
                )
            )

            model, labels = perform_kmeans(
                matrix,
                n_clusters=n_clusters
            )

            keywords = get_cluster_keywords(
                model,
                vectorizer,
                top_n=top_keywords
            )

            silhouette = (
                calculate_silhouette_score(
                    matrix,
                    labels
                )
            )

            distribution = (
                get_cluster_distribution(
                    labels
                )
            )

            topic_results = {
                "vectorizer": vectorizer,
                "matrix": matrix,
                "model": model,
                "labels": labels,
                "keywords": keywords,
                "silhouette": silhouette,
                "distribution": distribution,
                "texts": topic_text
            }

            st.session_state.topic_results = (
                topic_results
            )

        except ValueError as error:

            st.error(
                f"Unable to create topics: {error}"
            )

            st.stop()


results = st.session_state.get(
    "topic_results"
)


if results is None:

    st.info(
        "Configure the number of topics and click "
        "'Discover Topics'."
    )

    st.stop()


keywords = results["keywords"]

silhouette = results["silhouette"]

distribution = results["distribution"]


# Model quality

st.divider()

st.subheader("Model Overview")


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Messages Analyzed",
        len(results["labels"])
    )


with col2:

    st.metric(
        "Topics Discovered",
        len(keywords)
    )


with col3:

    if silhouette is not None:

        st.metric(
            "Silhouette Score",
            f"{silhouette:.3f}"
        )

    else:

        st.metric(
            "Silhouette Score",
            "N/A"
        )


# Topic distribution

st.divider()

st.subheader("Topic Distribution")


distribution_df = pd.DataFrame(
    {
        "Topic": [
            f"Topic {topic}"
            for topic in distribution.index
        ],
        "Messages": distribution.values
    }
).set_index("Topic")


st.bar_chart(
    distribution_df
)


# Topic keywords

st.divider()

st.subheader("Discovered Topics")


for topic_id, topic_words in keywords.items():

    topic_count = int(
        distribution.get(
            topic_id,
            0
        )
    )

    st.markdown(
        f"### Topic {topic_id + 1}"
    )

    st.write(
        f"Messages in this topic: {topic_count}"
    )

    st.write(
        "**Keywords:** "
        + ", ".join(topic_words)
    )


# Message assignments

st.divider()

st.subheader("Message Topic Assignments")


assignment_df = pd.DataFrame(
    {
        "message": results["texts"].values,
        "topic": results["labels"]
    }
)


assignment_df["topic"] = (
    assignment_df["topic"]
    .apply(lambda x: f"Topic {x + 1}")
)


st.dataframe(
    assignment_df,
    use_container_width=True
)