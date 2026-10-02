import pandas as pd


def get_total_messages(df):
    """Return total number of parsed messages."""
    return len(df)


def get_participants(df):
    """Return sorted list of participants."""
    return sorted(df["sender"].dropna().unique())


def get_participant_count(df):
    """Return number of unique participants."""
    return df["sender"].nunique()


def get_messages_per_user(df):
    """Return number of messages sent by each participant."""
    return (
        df["sender"]
        .value_counts()
        .sort_values(ascending=False)
    )


def get_words_per_user(df):
    """Return total words sent by each participant."""
    return (
        df.groupby("sender")["word_count"]
        .sum()
        .sort_values(ascending=False)
    )


def get_average_message_length(df):
    """Return average message length in characters."""
    return df["character_count"].mean()


def get_media_count(df):
    """Return total number of media messages."""
    return int(df["is_media"].sum())


def get_media_by_type(df):
    """Return media count grouped by media type."""
    return (
        df[df["is_media"]]["media_type"]
        .value_counts()
    )


def get_link_count(df):
    """Return total number of messages containing URLs."""
    return int(df["has_url"].sum())


def get_total_url_count(df):
    """Return total number of URLs found."""
    return int(df["url_count"].sum())


def get_most_active_user(df):
    """Return participant with the most messages."""
    messages = get_messages_per_user(df)

    if messages.empty:
        return None

    return messages.index[0]


def get_user_statistics(df):
    """
    Return a combined participant statistics DataFrame.
    """

    stats = (
        df.groupby("sender")
        .agg(
            messages=("message", "count"),
            words=("word_count", "sum"),
            average_message_length=("character_count", "mean"),
            media_messages=("is_media", "sum"),
            links=("has_url", "sum")
        )
        .sort_values("messages", ascending=False)
    )

    return stats