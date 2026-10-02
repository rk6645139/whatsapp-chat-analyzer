from src.parser import parse_whatsapp_chat
from src.preprocessing import preprocess_messages

from src.analytics import (
    get_total_messages,
    get_participants,
    get_participant_count,
    get_messages_per_user,
    get_words_per_user,
    get_average_message_length,
    get_media_count,
    get_link_count,
    get_total_url_count,
    get_most_active_user,
    get_user_statistics,
)


def get_data():

    df = parse_whatsapp_chat("tests/fixtures/sample_chat.txt")

    return preprocess_messages(df)


def test_total_messages():

    df = get_data()

    assert get_total_messages(df) > 0


def test_participants():

    df = get_data()

    participants = get_participants(df)

    assert len(participants) > 0


def test_participant_count():

    df = get_data()

    assert get_participant_count(df) > 0


def test_messages_per_user():

    df = get_data()

    result = get_messages_per_user(df)

    assert not result.empty


def test_words_per_user():

    df = get_data()

    result = get_words_per_user(df)

    assert not result.empty


def test_average_message_length():

    df = get_data()

    result = get_average_message_length(df)

    assert result >= 0


def test_media_count():

    df = get_data()

    result = get_media_count(df)

    assert result >= 0


def test_link_count():

    df = get_data()

    result = get_link_count(df)

    assert result >= 0


def test_total_url_count():

    df = get_data()

    result = get_total_url_count(df)

    assert result >= 0


def test_most_active_user():

    df = get_data()

    result = get_most_active_user(df)

    assert result is not None


def test_user_statistics():

    df = get_data()

    result = get_user_statistics(df)

    assert not result.empty