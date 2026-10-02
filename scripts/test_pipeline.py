from src.parser import parse_whatsapp_chat
from src.preprocessing import preprocess_messages


df = parse_whatsapp_chat("data/chat.txt")

print("\nRAW DATA")
print(df.head())

processed_df = preprocess_messages(df)

print("\nPROCESSED DATA")
print(processed_df.head())

print("\nCOLUMNS")
print(processed_df.columns.tolist())

print("\nMESSAGE TYPES")
print(processed_df["media_type"].value_counts(dropna=False))

print("\nDELETED MESSAGES")
print(processed_df["is_deleted"].sum())

print("\nURL MESSAGES")
print(processed_df["has_url"].sum())

print("\nPARTICIPANTS")
print(processed_df["sender"].nunique())