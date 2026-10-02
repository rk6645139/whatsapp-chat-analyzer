import pandas as pd
from transformers import pipeline


MODEL_NAME = "cardiffnlp/twitter-xlm-roberta-base-sentiment"


LABEL_MAP = {
    "LABEL_0": "negative",
    "LABEL_1": "neutral",
    "LABEL_2": "positive",
    "negative": "negative",
    "neutral": "neutral",
    "positive": "positive",
}


def load_sentiment_model():

    return pipeline(
        "sentiment-analysis",
        model=MODEL_NAME,
        tokenizer=MODEL_NAME
    )


def analyze_sentiment(
    df,
    model=None,
    text_column="message",
    batch_size=8
):

    if text_column not in df.columns:
        raise ValueError(
            f"Column '{text_column}' not found in DataFrame."
        )

    result = df.copy()

    result["sentiment"] = "not_applicable"
    result["sentiment_score"] = 0.0

    valid_mask = (
        ~result["is_media"]
        & ~result["is_deleted"]
        & result[text_column].notna()
        & result[text_column]
            .astype(str)
            .str.strip()
            .ne("")
    )

    valid_indices = result.index[
        valid_mask
    ]

    if model is None:
        model = load_sentiment_model()

    texts = (
        result.loc[
            valid_indices,
            text_column
        ]
        .astype(str)
        .tolist()
    )

    predictions = []

    for start in range(
        0,
        len(texts),
        batch_size
    ):

        batch = texts[
            start:start + batch_size
        ]

        batch_predictions = model(
            batch,
            truncation=True
        )

        predictions.extend(
            batch_predictions
        )

    for index, prediction in zip(
        valid_indices,
        predictions
    ):

        raw_label = prediction["label"]

        label = LABEL_MAP.get(
            raw_label,
            raw_label.lower()
        )

        result.at[
            index,
            "sentiment"
        ] = label

        result.at[
            index,
            "sentiment_score"
        ] = prediction["score"]

    return result


def get_valid_sentiment_data(df):

    if "sentiment" not in df.columns:
        return pd.DataFrame()

    return df[
        df["sentiment"] != "not_applicable"
    ].copy()


def get_sentiment_distribution(df):

    data = get_valid_sentiment_data(df)

    if data.empty:
        return pd.Series(dtype=int)

    return (
        data["sentiment"]
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


def get_sentiment_percentage(df):

    distribution = (
        get_sentiment_distribution(df)
    )

    if distribution.sum() == 0:
        return distribution

    return (
        distribution
        / distribution.sum()
        * 100
    ).round(2)


def get_sentiment_by_user(df):

    data = get_valid_sentiment_data(df)

    if data.empty:
        return pd.DataFrame()

    return pd.crosstab(
        data["sender"],
        data["sentiment"]
    )


def get_average_sentiment_score(df):

    data = get_valid_sentiment_data(df)

    if data.empty:
        return pd.Series(dtype=float)

    return (
        data.groupby("sentiment")[
            "sentiment_score"
        ]
        .mean()
        .round(3)
    )

def get_sentiment_over_time(df):

    data = get_valid_sentiment_data(df)

    if data.empty:
        return pd.DataFrame()

    result = (
        data.groupby(
            [
                data["datetime"].dt.date,
                "sentiment"
            ]
        )
        .size()
        .reset_index(
            name="messages"
        )
    )

    result = result.rename(
        columns={
            "datetime": "date"
        }
    )

    return result