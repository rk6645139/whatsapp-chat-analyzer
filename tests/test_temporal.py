from src.parser import parse_whatsapp_chat
from src.preprocessing import preprocess_messages

from src.temporal import (
    get_daily_activity,
    get_weekly_activity,
    get_monthly_activity,
    get_hourly_activity,
    get_day_of_week_activity,
    get_activity_heatmap,
    get_most_active_hour,
    get_most_active_day,
    get_activity_summary,
)


def get_data():

    df = parse_whatsapp_chat("data/chat.txt")

    return preprocess_messages(df)


def test_daily_activity():

    df = get_data()

    result = get_daily_activity(df)

    assert not result.empty
    assert "messages" in result.columns


def test_weekly_activity():

    df = get_data()

    result = get_weekly_activity(df)

    assert not result.empty


def test_monthly_activity():

    df = get_data()

    result = get_monthly_activity(df)

    assert not result.empty


def test_hourly_activity():

    df = get_data()

    result = get_hourly_activity(df)

    assert len(result) == 24


def test_day_of_week_activity():

    df = get_data()

    result = get_day_of_week_activity(df)

    assert len(result) == 7


def test_heatmap():

    df = get_data()

    result = get_activity_heatmap(df)

    assert result.shape == (7, 24)


def test_most_active_hour():

    df = get_data()

    result = get_most_active_hour(df)

    assert 0 <= result <= 23


def test_most_active_day():

    df = get_data()

    result = get_most_active_day(df)

    assert result in [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]


def test_activity_summary():

    df = get_data()

    result = get_activity_summary(df)

    assert "most_active_hour" in result
    assert "most_active_day" in result