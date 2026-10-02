import pandas as pd


def generate_conversation_summary(
    df,
    messages_per_user,
    activity_summary,
    word_frequency=None,
    sentiment_percentage=None,
    toxicity_percentage=None
):
    """
    Generate a structured conversation summary
    from computed analytics.
    """

    summary = {}

    # -------------------------
    # Basic statistics
    # -------------------------

    summary["total_messages"] = len(df)

    summary["total_participants"] = (
        df["sender"].nunique()
    )

    # -------------------------
    # Most active user
    # -------------------------

    if not messages_per_user.empty:

        summary["most_active_user"] = (
            messages_per_user.index[0]
        )

        summary["most_active_user_messages"] = (
            int(messages_per_user.iloc[0])
        )

    else:

        summary["most_active_user"] = None
        summary["most_active_user_messages"] = 0

    # -------------------------
    # Activity
    # -------------------------

    summary["most_active_hour"] = (
        activity_summary.get(
            "most_active_hour"
        )
    )

    summary["most_active_day"] = (
        activity_summary.get(
            "most_active_day"
        )
    )

    summary["active_hours"] = (
        activity_summary.get(
            "active_hours"
        )
    )

    # -------------------------
    # Word statistics
    # -------------------------

    if word_frequency:

        summary["top_words"] = [
            word
            for word, count
            in word_frequency[:10]
        ]

    else:

        summary["top_words"] = []

    # -------------------------
    # Sentiment
    # -------------------------

    if sentiment_percentage is not None:

        summary["sentiment_percentage"] = (
            sentiment_percentage.to_dict()
        )

    else:

        summary["sentiment_percentage"] = {}

    # -------------------------
    # Toxicity
    # -------------------------

    if toxicity_percentage is not None:

        summary["toxicity_percentage"] = (
            toxicity_percentage.to_dict()
        )

    else:

        summary["toxicity_percentage"] = {}

    return summary


def format_summary(summary):
    """
    Convert the structured summary into
    human-readable bullet points.
    """

    lines = []

    lines.append(
        f"Total messages: "
        f"{summary['total_messages']}"
    )

    lines.append(
        f"Participants: "
        f"{summary['total_participants']}"
    )

    if summary["most_active_user"]:

        lines.append(
            f"Most active participant: "
            f"{summary['most_active_user']} "
            f"({summary['most_active_user_messages']} messages)"
        )

    if summary["most_active_day"]:

        lines.append(
            f"Most active day: "
            f"{summary['most_active_day']}"
        )

    if summary["most_active_hour"] is not None:

        hour = summary["most_active_hour"]

        lines.append(
            f"Most active hour: "
            f"{hour}:00"
        )

    if summary["top_words"]:

        lines.append(
            "Top words: "
            + ", ".join(
                summary["top_words"]
            )
        )

    return lines