from src.parser import parse_whatsapp_chat
from src.preprocessing import preprocess_messages
from src.toxicity import (
    load_toxicity_model,
    analyze_toxicity
)


df = parse_whatsapp_chat("data/chat.txt")

df = preprocess_messages(df)

model = load_toxicity_model()

result = analyze_toxicity(
    df.head(20),
    model=model
)

print(
    result[
        [
            "sender",
            "message",
            "toxicity_label",
            "toxicity_score"
        ]
    ].to_string(index=False)
)