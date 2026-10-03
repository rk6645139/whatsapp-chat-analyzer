import re
from collections import Counter
import nltk
import emoji


# --------------------------------------------------
# Stopwords
# --------------------------------------------------


from nltk.corpus import stopwords

try:
    ENGLISH_STOPWORDS = set(stopwords.words("english"))
except LookupError:
    nltk.download("stopwords", quiet=True)
    
    ENGLISH_STOPWORDS = set(stopwords.words("english"))


CUSTOM_STOPWORDS = {
    "hai",
    "h",
    "kr",
    "k",
    "ka",
    "ke",
    "ki",
    "mt",
    "mein",
    "me",
    "nhi",
    "toh",
    "bhi",
    "ya",
    "se",
    "ko",
    "ho",
    "rha",
    "raha",
    "hoga",
}

STOPWORDS = ENGLISH_STOPWORDS.union(CUSTOM_STOPWORDS)


# --------------------------------------------------
# Text cleaning
# --------------------------------------------------

def clean_text(text):
    """
    Clean a message for text-frequency/NLP analysis.

    Keeps Unicode letters and numbers so Hindi and
    other non-English text are not automatically removed.
    """

    if not isinstance(text, str):
        return ""

    # Remove URLs
    text = re.sub(
        r"https?://\S+|www\.\S+",
        " ",
        text
    )

    # Remove emojis
    text = emoji.replace_emoji(
        text,
        replace=""
    )

    # Convert to lowercase
    text = text.lower()

    # Keep Unicode word characters
    text = re.sub(
        r"[^\w\s]",
        " ",
        text,
        flags=re.UNICODE
    )

    # Normalize whitespace
    text = re.sub(
        r"\s+",
        " ",
        text
    ).strip()

    return text


# --------------------------------------------------
# Tokenization
# --------------------------------------------------

def tokenize_text(text):
    """
    Convert cleaned text into tokens.
    """

    cleaned = clean_text(text)

    if not cleaned:
        return []

    return cleaned.split()


# --------------------------------------------------
# Stopword removal
# --------------------------------------------------

def remove_stopwords(tokens):
    """
    Remove configured stopwords.
    """

    return [
        token
        for token in tokens
        if token not in STOPWORDS
    ]


# --------------------------------------------------
# Word frequency
# --------------------------------------------------

def get_word_frequency(df, user=None, top_n=20):
    """
    Return most frequent words.

    user:
        If supplied, analyze only that participant.
    """

    data = df

    if user is not None:
        data = data[data["sender"] == user]

    counter = Counter()

    for message in data["message"]:
        tokens = tokenize_text(message)
        tokens = remove_stopwords(tokens)

        counter.update(tokens)

    return counter.most_common(top_n)


# --------------------------------------------------
# Unique words
# --------------------------------------------------

def get_unique_word_count(df, user=None):
    """
    Return number of unique cleaned words.
    """

    data = df

    if user is not None:
        data = data[data["sender"] == user]

    words = set()

    for message in data["message"]:
        tokens = tokenize_text(message)
        tokens = remove_stopwords(tokens)

        words.update(tokens)

    return len(words)


# --------------------------------------------------
# Emoji extraction
# --------------------------------------------------

def extract_emojis(text):
    """
    Extract emojis from a message.
    """

    if not isinstance(text, str):
        return []

    return [
        character
        for character in text
        if character in emoji.EMOJI_DATA
    ]


def get_emoji_frequency(df, user=None, top_n=20):
    """
    Return most frequently used emojis.
    """

    data = df

    if user is not None:
        data = data[data["sender"] == user]

    counter = Counter()

    for message in data["message"]:
        counter.update(extract_emojis(message))

    return counter.most_common(top_n)


def get_total_emoji_count(df, user=None):
    """
    Return total number of emojis.
    """

    data = df

    if user is not None:
        data = data[data["sender"] == user]

    total = 0

    for message in data["message"]:
        total += len(extract_emojis(message))

    return total


# --------------------------------------------------
# Emoji counts by user
# --------------------------------------------------

def get_emoji_count_by_user(df):
    """
    Return total emoji usage per participant.
    """

    result = {}

    for user, group in df.groupby("sender"):

        count = get_total_emoji_count(group)

        result[user] = count

    return result


# --------------------------------------------------
# Basic NLP statistics
# --------------------------------------------------

def get_average_words_per_message(df):
    """
    Return average number of words per message.
    """

    if df.empty:
        return 0

    return df["word_count"].mean()


def get_longest_messages(df, top_n=10):
    """
    Return longest messages by character count.
    """

    return (
        df[
            [
                "sender",
                "message",
                "character_count"
            ]
        ]
        .sort_values(
            "character_count",
            ascending=False
        )
        .head(top_n)
    )