from src.parser import parse_whatsapp_chat
from src.preprocessing import preprocess_messages

from src.nlp import (
    get_word_frequency,
    get_unique_word_count,
    get_emoji_frequency,
    get_total_emoji_count,
    get_emoji_count_by_user,
    get_average_words_per_message,
    get_longest_messages,
)


df = parse_whatsapp_chat("data/chat.txt")

df = preprocess_messages(df)


print("\n========== TOP WORDS ==========")

for word, count in get_word_frequency(df):
    print(f"{word}: {count}")


print("\n========== UNIQUE WORDS ==========")

print(get_unique_word_count(df))


print("\n========== TOP EMOJIS ==========")

for emoji_character, count in get_emoji_frequency(df):
    print(f"{emoji_character}: {count}")


print("\n========== TOTAL EMOJIS ==========")

print(get_total_emoji_count(df))


print("\n========== EMOJIS BY USER ==========")

print(get_emoji_count_by_user(df))


print("\n========== AVERAGE WORDS ==========")

print(
    round(
        get_average_words_per_message(df),
        2
    )
)


print("\n========== LONGEST MESSAGES ==========")

print(get_longest_messages(df))