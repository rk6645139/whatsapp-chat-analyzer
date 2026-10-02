import streamlit as st


st.title("WhatsApp Chat Analyzer")

st.caption(
    "NLP & Conversation Analytics Platform"
)

st.divider()

st.header("Welcome")

st.write(
    """
    Upload a WhatsApp chat export from the sidebar
    to begin analyzing your conversation.
    """
)

st.info(
    "Upload a WhatsApp .txt file using the sidebar."
)