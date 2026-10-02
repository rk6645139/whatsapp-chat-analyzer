from src.parser import parse_whatsapp_chat
from src.preprocessing import preprocess_messages
from src.search import (
    search_messages,
    format_search_results,
    get_conversation_context
)


# Load chat
df = parse_whatsapp_chat("data/chat.txt")

# Preprocess
df = preprocess_messages(df)


# -------------------------
# Test 1: Keyword search
# -------------------------

results = search_messages(
    df,
    query="college"
)
print("Keyword search results:")
print("Number of results:", len(results))

print(
    format_search_results(
        results
    ).to_string(index=False)
)


# -------------------------
# Test 2: User + keyword
# -------------------------

if not df.empty:

    user = df["sender"].iloc[0]

    results = search_messages(
        df,
        query="resume",
        user=user
    )

    print("\nUser + keyword results:")
    print("User:", user)
    print("Number of results:", len(results))


# -------------------------
# Test 3: Conversation context
# -------------------------

if not results.empty:

    context = get_conversation_context(
        results,
        message_index=0,
        context_size=2
    )

    print("\nConversation context:")
    print(
        context.to_string(index=False)
    )