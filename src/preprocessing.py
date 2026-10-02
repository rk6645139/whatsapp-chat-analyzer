import re

import pandas as pd


# Common WhatsApp media placeholders
MEDIA_TYPES = {
    "<media omitted>": "media",
    "<image omitted>": "image",
    "<video omitted>": "video",
    "<audio omitted>": "audio",
    "<sticker omitted>": "sticker",
    "<document omitted>": "document",
}


def preprocess_messages(df):
    """
    Clean and enrich parsed WhatsApp messages.

    Parameters:
        df: DataFrame produced by parser.py

    Returns:
        Enriched DataFrame
    """

    df = df.copy()

    # --------------------------------------------------
    # 1. Basic validation
    # --------------------------------------------------

    required_columns = {
        "date",
        "time",
        "sender",
        "message"
    }

    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    # --------------------------------------------------
    # 2. Clean text columns
    # --------------------------------------------------

    df["sender"] = df["sender"].astype(str).str.strip()
    df["message"] = df["message"].astype(str).str.strip()

    # --------------------------------------------------
    # 3. Deleted messages
    # --------------------------------------------------

    df["is_deleted"] = (
        df["message"].str.lower()
        == "this message was deleted"
    )

    # --------------------------------------------------
    # 4. Media detection
    # --------------------------------------------------

    df["media_type"] = df["message"].map(MEDIA_TYPES)

    df["is_media"] = df["media_type"].notna()

    # --------------------------------------------------
    # 5. Date + time
    # --------------------------------------------------

    datetime_text = (
        df["date"].astype(str)
        + ", "
        + df["time"].astype(str)
)

    df["datetime"] = pd.to_datetime(
        datetime_text,
        dayfirst=True,
        errors="coerce"
)


    # --------------------------------------------------
    # 6. URL detection
    # --------------------------------------------------

    url_pattern = r"https?://\S+|www\.\S+"

    df["has_url"] = df["message"].str.contains(
        url_pattern,
        regex=True,
        case=False,
        na=False
    )

    df["url_count"] = df["message"].str.count(
        url_pattern
    )

    # --------------------------------------------------
    # 7. Word count
    # --------------------------------------------------

    df["word_count"] = (
        df["message"]
        .where(
            ~df["is_media"]
            & ~df["is_deleted"],
            ""
    )
        .str.split()
        .str.len()
        .fillna(0)
        .astype(int)
)

    df["character_count"] = (
        df["message"]
        .where(
            ~df["is_media"]
            & ~df["is_deleted"],
         ""
    )
    .str.len()
    .fillna(0)
    .astype(int)
)
    # --------------------------------------------------
    # 9. Date/time features
    # --------------------------------------------------

    df["year"] = df["datetime"].dt.year
    df["month"] = df["datetime"].dt.month
    df["day"] = df["datetime"].dt.day
    df["hour"] = df["datetime"].dt.hour
    df["day_of_week"] = df["datetime"].dt.day_name()

    return df