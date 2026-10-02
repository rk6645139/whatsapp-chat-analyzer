import pandas as pd

from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import silhouette_score


def prepare_topic_text(df):

    text = (
        df["message"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    valid_mask = (
        ~df["is_media"]
        & ~df["is_deleted"]
        & text.ne("")
    )

    return text[valid_mask]


def create_tfidf_matrix(
    texts,
    max_features=1000,
    min_df=2,
    max_df=0.95
):

    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=max_features,
        min_df=min_df,
        max_df=max_df,
        ngram_range=(1, 2)
    )

    matrix = vectorizer.fit_transform(texts)

    return vectorizer, matrix


def perform_kmeans(
    matrix,
    n_clusters=5,
    random_state=42
):

    model = KMeans(
        n_clusters=n_clusters,
        random_state=random_state,
        n_init=10
    )

    labels = model.fit_predict(matrix)

    return model, labels


def get_cluster_keywords(
    model,
    vectorizer,
    top_n=10
):

    feature_names = (
        vectorizer
        .get_feature_names_out()
    )

    cluster_keywords = {}

    for cluster_id, center in enumerate(
        model.cluster_centers_
    ):

        top_indices = (
            center
            .argsort()[::-1][:top_n]
        )

        words = [
            feature_names[index]
            for index in top_indices
        ]

        cluster_keywords[cluster_id] = words

    return cluster_keywords


def calculate_silhouette_score(
    matrix,
    labels
):

    unique_labels = len(
        set(labels)
    )

    if unique_labels < 2:
        return None

    if unique_labels >= matrix.shape[0]:
        return None

    return silhouette_score(
        matrix,
        labels
    )


def get_cluster_distribution(labels):

    return (
        pd.Series(labels)
        .value_counts()
        .sort_index()
    )