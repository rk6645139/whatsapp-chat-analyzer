import pandas as pd


def prepare_response_data(df):
    required_columns = {
        "datetime",
        "sender",
        "message",
        "is_media",
        "is_deleted"
    }

    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    result = df.copy()

    result = result[
        ~result["is_media"]
        & ~result["is_deleted"]
    ].copy()

    result = result[
        result["datetime"].notna()
    ].copy()

    result = result[
        result["message"].astype(str).str.strip().ne("")
    ].copy()

    result = (
        result
        .sort_values("datetime")
        .reset_index(drop=True)
    )

    return result


def calculate_response_times(
    df,
    max_gap_minutes=60
):
    data = prepare_response_data(df)

    responses = []

    for i in range(1, len(data)):

        previous = data.iloc[i - 1]
        current = data.iloc[i]

        if previous["sender"] == current["sender"]:
            continue

        response_time = (
            current["datetime"]
            - previous["datetime"]
        ).total_seconds() / 60

        if response_time <= 0:
            continue

        if response_time > max_gap_minutes:
            continue

        responses.append(
            {
                "from_user": previous["sender"],
                "to_user": current["sender"],
                "previous_message": previous["message"],
                "response_message": current["message"],
                "previous_datetime": previous["datetime"],
                "response_datetime": current["datetime"],
                "response_time_minutes": response_time
            }
        )

    return pd.DataFrame(responses)


def get_average_response_time(response_df):

    if response_df.empty:
        return 0.0

    return response_df[
        "response_time_minutes"
    ].mean()


def get_median_response_time(response_df):

    if response_df.empty:
        return 0.0

    return response_df[
        "response_time_minutes"
    ].median()


def get_fastest_response(response_df):

    if response_df.empty:
        return 0.0

    return response_df[
        "response_time_minutes"
    ].min()


def get_slowest_response(response_df):

    if response_df.empty:
        return 0.0

    return response_df[
        "response_time_minutes"
    ].max()


def get_response_time_by_user(response_df):

    if response_df.empty:
        return pd.DataFrame()

    return (
        response_df
        .groupby("to_user")[
            "response_time_minutes"
        ]
        .agg(
            responses="count",
            average_response_time="mean",
            median_response_time="median",
            fastest_response="min",
            slowest_response="max"
        )
        .sort_values(
            "average_response_time"
        )
    )


def get_response_matrix(response_df):

    if response_df.empty:
        return pd.DataFrame()

    return pd.crosstab(
        response_df["from_user"],
        response_df["to_user"]
    )