from src.parser import parse_whatsapp_chat
from src.preprocessing import preprocess_messages


def get_processed_data():
    df = parse_whatsapp_chat("tests/fixtures/sample_chat.txt")
    return preprocess_messages(df)


def test_preprocessing_returns_dataframe():

    df = get_processed_data()

    assert not df.empty


def test_datetime_column_exists():

    df = get_processed_data()

    assert "datetime" in df.columns


def test_deleted_messages_are_detected():

    df = get_processed_data()

    deleted_messages = df[df["is_deleted"]]

    assert len(deleted_messages) > 0


def test_media_messages_are_detected():

    df = get_processed_data()

    media_messages = df[df["is_media"]]

    assert len(media_messages) > 0


def test_url_detection():

    df = get_processed_data()

    url_messages = df[df["has_url"]]

    assert len(url_messages) > 0