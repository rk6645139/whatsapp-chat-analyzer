from src.parser import parse_whatsapp_chat
from src.preprocessing import preprocess_messages
from src.sentiment import load_sentiment_model, analyze_sentiment


df = parse_whatsapp_chat("data/chat.txt")

df = preprocess_messages(df)

model = load_sentiment_model()

result = analyze_sentiment(
    df.head(20),
    model=model
)

print(
    result[
        [
            "sender",
            "message",
            "sentiment",
            "sentiment_score"
        ]
    ].to_string(index=False)
)