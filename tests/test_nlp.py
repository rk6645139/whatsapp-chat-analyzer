from src.parser import parse_whatsapp_chat
from src.preprocessing import preprocess_messages

from src.nlp import (
    clean_text,
    tokenize_text,
    remove_stopwords,
    get_word_frequency,
    get_unique_word_count,
    extract_emojis,
    get_emoji_frequency,
    get_total_emoji_count,
    get_emoji_count_by_user,
    get_average_words_per_message,
    get_longest_messages,
)


def get_data():

    df = parse_whatsapp_chat("data/chat.txt")

    return preprocess_messages(df)


def test_clean_text():

    text = "Hello 😁 https://example.com"

    result = clean_text(text)

    assert "https" not in result
    assert "😁" not in result
    assert "hello" in result


def test_tokenize_text():

    result = tokenize_text("Hello world")

    assert result == ["hello", "world"]


def test_remove_stopwords():

    tokens = ["this", "is", "a", "test"]

    result = remove_stopwords(tokens)

    assert "this" not in result
    assert "is" not in result


def test_word_frequency():

    df = get_data()

    result = get_word_frequency(df)

    assert isinstance(result, list)


def test_unique_word_count():

    df = get_data()

    result = get_unique_word_count(df)

    assert result >= 0


def test_extract_emojis():

    result = extract_emojis("Hello 😁 😂")

    assert "😁" in result
    assert "😂" in result


def test_emoji_frequency():

    df = get_data()

    result = get_emoji_frequency(df)

    assert isinstance(result, list)


def test_total_emoji_count():

    df = get_data()

    result = get_total_emoji_count(df)

    assert result >= 0


def test_emoji_count_by_user():

    df = get_data()

    result = get_emoji_count_by_user(df)

    assert isinstance(result, dict)


def test_average_words():

    df = get_data()

    result = get_average_words_per_message(df)

    assert result >= 0


def test_longest_messages():

    df = get_data()

    result = get_longest_messages(df)

    assert len(result) <= 10