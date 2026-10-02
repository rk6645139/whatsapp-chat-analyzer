import pandas as pd


def search_messages(
    df,
    query="",
    user=None,
    start_date=None,
    end_date=None,
    sentiment=None,
    toxicity=None,
    include_media=True,
    include_deleted=False
):

    result = df.copy()

    # Keyword search
    if query and query.strip():

        result = result[
            result["message"]
            .astype(str)
            .str.contains(
                query.strip(),
                case=False,
                na=False,
                regex=False
            )
        ]

    # Participant
    if user and user != "All":

        result = result[
            result["sender"] == user
        ]

    # Date range
    if start_date is not None:

        result = result[
            result["datetime"].notna()
    ]

        result = result[
            result["datetime"].dt.date
            >= start_date
    ]


    if end_date is not None:

        result = result[
            result["datetime"].notna()
        ]

        result = result[
            result["datetime"].dt.date
            <= end_date
    ]

    # Sentiment
    if (
        sentiment
        and sentiment != "All"
        and "sentiment" in result.columns
    ):

        result = result[
            result["sentiment"] == sentiment
        ]

    # Toxicity
    if (
        toxicity
        and toxicity != "All"
        and "toxicity_label" in result.columns
    ):

        result = result[
            result["toxicity_label"] == toxicity
        ]

    # Media
    if not include_media:

        result = result[
            ~result["is_media"]
        ]

    # Deleted
    if not include_deleted:

        result = result[
            ~result["is_deleted"]
        ]

    return (
        result
        .sort_values("datetime")
        .reset_index(drop=True)
    )


def format_search_results(df):

    columns = [
        "datetime",
        "sender",
        "message"
    ]

    available_columns = [
        column
        for column in columns
        if column in df.columns
    ]

    return df[
        available_columns
    ].copy()


def get_conversation_context(
    df,
    message_index,
    context_size=2
):

    if df.empty:
        return df.copy()

    if (
        message_index < 0
        or message_index >= len(df)
    ):

        raise IndexError(
            "message_index is outside "
            "the DataFrame range."
        )

    start = max(
        0,
        message_index - context_size
    )

    end = min(
        len(df),
        message_index + context_size + 1
    )

    columns = [
        "datetime",
        "sender",
        "message"
    ]

    available_columns = [
        column
        for column in columns
        if column in df.columns
    ]

    return df.iloc[
        start:end
    ][available_columns].copy()