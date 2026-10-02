from src.parser import parse_whatsapp_chat


def test_parser_returns_dataframe():

    df = parse_whatsapp_chat("tests/fixtures/sample_chat.txt")

    assert not df.empty


def test_required_columns_exist():

    df=parse_whatsapp_chat("tests/fixtures/sample_chat.txt")

    required_columns = {
        "date",
        "time",
        "sender",
        "message"
    }

    assert required_columns.issubset(df.columns)


def test_messages_have_senders():

    df=parse_whatsapp_chat("tests/fixtures/sample_chat.txt")

    assert df["sender"].notna().all()


def test_messages_have_content():

    df=parse_whatsapp_chat("tests/fixtures/sample_chat.txt")

    assert df["message"].notna().all()