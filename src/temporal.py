import pandas as pd


DAY_ORDER = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]


def get_daily_activity(df):
    """Return number of messages sent each day."""

    return (
        df.groupby(df["datetime"].dt.date)
        .size()
        .rename("messages")
        .reset_index(name="messages")
        .rename(columns={"datetime": "date"})
    )


def get_weekly_activity(df):
    """Return number of messages grouped by week."""

    result = (
        df.set_index("datetime")
        .resample("W")
        .size()
        .reset_index(name="messages")
    )

    return result


def get_monthly_activity(df):
    """Return number of messages grouped by month."""

    result = (
        df.set_index("datetime")
        .resample("ME")
        .size()
        .reset_index(name="messages")
    )

    return result


def get_hourly_activity(df):
    """Return number of messages for each hour of the day."""

    return (
        df.groupby("hour")
        .size()
        .reindex(range(24), fill_value=0)
        .rename("messages")
        .reset_index()
    )


def get_day_of_week_activity(df):
    """Return message count for each day of the week."""

    result = (
        df.groupby("day_of_week")
        .size()
        .reindex(DAY_ORDER, fill_value=0)
        .rename("messages")
        .reset_index()
    )

    return result


def get_activity_heatmap(df):
    """
    Return a day-of-week × hour activity matrix.
    """

    heatmap = pd.crosstab(
        df["day_of_week"],
        df["hour"]
    )

    heatmap = heatmap.reindex(
        index=DAY_ORDER,
        columns=range(24),
        fill_value=0
    )

    return heatmap


def get_most_active_hour(df):
    """Return the hour with the highest message count."""

    hourly = get_hourly_activity(df)

    return int(
        hourly.loc[
            hourly["messages"].idxmax(),
            "hour"
        ]
    )


def get_most_active_day(df):
    """Return the day of week with the highest activity."""

    daily = get_day_of_week_activity(df)

    return daily.loc[
        daily["messages"].idxmax(),
        "day_of_week"
    ]


def get_activity_summary(df):
    """Return useful temporal summary statistics."""

    hourly = get_hourly_activity(df)
    weekday = get_day_of_week_activity(df)

    return {
        "most_active_hour": int(
            hourly.loc[
                hourly["messages"].idxmax(),
                "hour"
            ]
        ),
        "most_active_day": weekday.loc[
            weekday["messages"].idxmax(),
            "day_of_week"
        ],
        "active_hours": int(
            (hourly["messages"] > 0).sum()
        ),
    }