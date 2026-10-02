from src.parser import parse_whatsapp_chat
from src.preprocessing import preprocess_messages

from src.temporal import (
    get_daily_activity,
    get_weekly_activity,
    get_monthly_activity,
    get_hourly_activity,
    get_day_of_week_activity,
    get_activity_heatmap,
    get_activity_summary,
)


df = parse_whatsapp_chat("data/chat.txt")

df = preprocess_messages(df)


print("\n========== DAILY ACTIVITY ==========")
print(get_daily_activity(df))


print("\n========== WEEKLY ACTIVITY ==========")
print(get_weekly_activity(df))


print("\n========== MONTHLY ACTIVITY ==========")
print(get_monthly_activity(df))


print("\n========== HOURLY ACTIVITY ==========")
print(get_hourly_activity(df))


print("\n========== DAY OF WEEK ==========")
print(get_day_of_week_activity(df))


print("\n========== HEATMAP DATA ==========")
print(get_activity_heatmap(df))


print("\n========== SUMMARY ==========")
print(get_activity_summary(df))