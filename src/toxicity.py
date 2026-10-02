import pandas as pd
from transformers import pipeline


MODEL_NAME = "unitary/toxic-bert"


def load_toxicity_model():
    return pipeline(
        "text-classification",
        model=MODEL_NAME,
        tokenizer=MODEL_NAME
    )


def analyze_toxicity(
    df,
    model=None,
    text_column="message",
    batch_size=8
):
    if text_column not in df.columns:
        raise ValueError(f"Column '{text_column}' not found in DataFrame.")

    result = df.copy()

    result["toxicity_label"] = "not_applicable"
    result["toxicity_score"] = 0.0

    valid_mask = (
        ~result["is_media"]
        & ~result["is_deleted"]
        & result[text_column].notna()
        & result[text_column].astype(str).str.strip().ne("")
    )

    valid_indices = result.index[valid_mask]

    if model is None:
        model = load_toxicity_model()

    texts = (
        result.loc[valid_indices, text_column]
        .astype(str)
        .tolist()
    )

    predictions = []

    for start in range(0, len(texts), batch_size):
        batch = texts[start:start + batch_size]

        batch_predictions = model(
            batch,
            truncation=True
        )

        predictions.extend(batch_predictions)

    for index, prediction in zip(valid_indices, predictions):

        score = prediction["score"]

        if (
            prediction["label"].lower() == "toxic"
            and score >= 0.50
        ):
            label = "toxic"
        else:
            label = "non-toxic"

        result.at[index, "toxicity_label"] = label
        result.at[index, "toxicity_score"] = score

    return result


def get_valid_toxicity_data(df):

    if "toxicity_label" not in df.columns:
        return pd.DataFrame()

    return df[
        df["toxicity_label"] != "not_applicable"
    ].copy()


def get_toxicity_distribution(df):

    data = get_valid_toxicity_data(df)

    if data.empty:
        return pd.Series(dtype=int)

    return (
        data["toxicity_label"]
        .value_counts()
        .reindex(
            ["non-toxic", "toxic"],
            fill_value=0
        )
    )


def get_toxicity_percentage(df):

    distribution = get_toxicity_distribution(df)

    if distribution.sum() == 0:
        return distribution

    return (
        distribution
        / distribution.sum()
        * 100
    ).round(2)


def get_toxicity_by_user(df):

    data = get_valid_toxicity_data(df)

    if data.empty:
        return pd.DataFrame()

    return pd.crosstab(
        data["sender"],
        data["toxicity_label"]
    )


def get_toxic_messages(df):

    data = get_valid_toxicity_data(df)

    if data.empty:
        return pd.DataFrame()

    return (
        data[data["toxicity_label"] == "toxic"]
        [
            [
                "datetime",
                "sender",
                "message",
                "toxicity_score"
            ]
        ]
        .sort_values(
            "toxicity_score",
            ascending=False
        )
    )