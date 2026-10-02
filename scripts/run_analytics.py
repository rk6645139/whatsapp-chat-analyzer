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
    get_media_by_type,
    get_link_count,
    get_total_url_count,
    get_most_active_user,
    get_user_statistics,
)


df = parse_whatsapp_chat("data/chat.txt")

df = preprocess_messages(df)


print("\n========== OVERVIEW ==========")

print("Total messages:", get_total_messages(df))

print("Participants:", get_participant_count(df))

print("Participant names:")

for participant in get_participants(df):
    print("-", participant)


print("\n========== MESSAGES PER USER ==========")

print(get_messages_per_user(df))


print("\n========== WORDS PER USER ==========")

print(get_words_per_user(df))


print("\n========== MESSAGE LENGTH ==========")

print(
    "Average characters:",
    round(get_average_message_length(df), 2)
)


print("\n========== MEDIA ==========")

print("Total media:", get_media_count(df))

print(get_media_by_type(df))


print("\n========== LINKS ==========")

print("Messages containing links:", get_link_count(df))

print("Total URLs:", get_total_url_count(df))


print("\n========== MOST ACTIVE USER ==========")

print(get_most_active_user(df))


print("\n========== USER STATISTICS ==========")

print(get_user_statistics(df))