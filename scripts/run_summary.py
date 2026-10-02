from src.parser import parse_whatsapp_chat
from src.preprocessing import preprocess_messages

from src.analytics import (
    get_messages_per_user
)

from src.temporal import (
    get_activity_summary
)

from src.nlp import (
    get_word_frequency
)

from src.summary import (
    generate_conversation_summary,
    format_summary
)


# -------------------------
# Load chat
# -------------------------

df = parse_whatsapp_chat(
    "data/chat.txt"
)

# -------------------------
# Preprocess
# -------------------------

df = preprocess_messages(df)


# -------------------------
# Analytics
# -------------------------

messages_per_user = (
    get_messages_per_user(df)
)


# -------------------------
# Temporal analysis
# -------------------------

activity_summary = (
    get_activity_summary(df)
)


# -------------------------
# NLP
# -------------------------

word_frequency = (
    get_word_frequency(
        df,
        top_n=10
    )
)


# -------------------------
# Generate summary
# -------------------------

summary = generate_conversation_summary(
    df=df,
    messages_per_user=messages_per_user,
    activity_summary=activity_summary,
    word_frequency=word_frequency
)


# -------------------------
# Display
# -------------------------

print("\nCONVERSATION SUMMARY")
print("=" * 50)

for line in format_summary(summary):
    print("•", line)