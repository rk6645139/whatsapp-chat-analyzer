import streamlit as st

from src.parser import parse_whatsapp_chat
from src.preprocessing import preprocess_messages


@st.cache_data
def load_chat_data(file_bytes):
    temp_file = "data/temp_chat.txt"

    with open(temp_file, "wb") as file:
        file.write(file_bytes)

    df = parse_whatsapp_chat(temp_file)
    df = preprocess_messages(df)

    return df