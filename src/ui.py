# import streamlit as st
# import tempfile
# import os


# from src.parser import parse_whatsapp_chat
# from src.preprocessing import preprocess_messages


# def load_chat(uploaded_file):

#     try:

#         file_bytes = uploaded_file.getvalue()

#         with tempfile.NamedTemporaryFile(
#             mode="wb",
#             suffix=".txt",
#             delete=False
#         ) as temp_file:

#             temp_file.write(file_bytes)
#             temp_path = temp_file.name

#         df = parse_whatsapp_chat(
#             temp_path
#         )

#         df = preprocess_messages(
#             df
#         )
#         os.remove(temp_path)

#         return df

#     except Exception as error:

#         st.error(
#             f"Unable to process chat: {error}"
#         )

#         return None


# def render_sidebar():

#     st.sidebar.title("WhatsApp Analyzer")

#     if "chat_df" not in st.session_state:
#         st.session_state.chat_df = None

#     uploaded_file = st.sidebar.file_uploader(
#         "Upload WhatsApp Chat",
#         type=["txt"]
#     )

#     if uploaded_file is not None:

#         if (
#             st.session_state.chat_df is None
#             or st.session_state.get("uploaded_file_name")
#             != uploaded_file.name
#         ):

#             with st.spinner(
#                 "Processing chat..."
#             ):

#                 df = load_chat(
#                     uploaded_file
#                 )

#                 st.session_state.chat_df = df

#                 st.session_state.uploaded_file_name = (
#                     uploaded_file.name
#                 )

#     df = st.session_state.chat_df

#     if df is not None:

#         st.sidebar.success(
#             "Chat loaded successfully"
#         )

#         st.sidebar.caption(
#             f"File: "
#             f"{st.session_state.uploaded_file_name}"
#         )

#         st.sidebar.divider()

#         if st.sidebar.button("Clear Chat"):

#             st.session_state.chat_df = None

#             if "uploaded_file_name" in st.session_state:
#                 del st.session_state.uploaded_file_name

#             st.rerun()

#     return df



import os
import tempfile

import streamlit as st

from src.parser import parse_whatsapp_chat
from src.preprocessing import preprocess_messages


def load_chat(uploaded_file):

    temp_path = None

    try:

        file_bytes = uploaded_file.getvalue()

        with tempfile.NamedTemporaryFile(
            mode="wb",
            suffix=".txt",
            delete=False
        ) as temp_file:

            temp_file.write(file_bytes)
            temp_path = temp_file.name

        df = parse_whatsapp_chat(
            temp_path
        )

        df = preprocess_messages(
            df
        )

        return df

    except Exception as error:

        st.error(
            f"Unable to process chat: {error}"
        )

        return None

    finally:

        if (
            temp_path is not None
            and os.path.exists(temp_path)
        ):
            os.remove(temp_path)


def reset_analysis_state():

    keys_to_clear = [
        "sentiment_df",
        "toxicity_df",
        "topic_results",
        "response_df"
    ]

    for key in keys_to_clear:

        if key in st.session_state:
            del st.session_state[key]


def render_sidebar():

    st.sidebar.title(
        "WhatsApp Analyzer"
    )

    if "chat_df" not in st.session_state:
        st.session_state.chat_df = None

    uploaded_file = st.sidebar.file_uploader(
        "Upload WhatsApp Chat",
        type=["txt"]
    )

    if uploaded_file is not None:

        previous_file = st.session_state.get(
            "uploaded_file_name"
        )

        if (
            st.session_state.chat_df is None
            or previous_file != uploaded_file.name
        ):

            with st.spinner(
                "Processing chat..."
            ):

                df = load_chat(
                    uploaded_file
                )

            if df is not None:

                reset_analysis_state()

                st.session_state.chat_df = df

                st.session_state.uploaded_file_name = (
                    uploaded_file.name
                )

    df = st.session_state.chat_df

    if df is not None:

        st.sidebar.success(
            "Chat loaded successfully"
        )

        st.sidebar.caption(
            f"File: "
            f"{st.session_state.uploaded_file_name}"
        )

        st.sidebar.divider()

        if st.sidebar.button(
            "Clear Chat"
        ):

            reset_analysis_state()

            st.session_state.chat_df = None

            if (
                "uploaded_file_name"
                in st.session_state
            ):
                del st.session_state[
                    "uploaded_file_name"
                ]

            st.rerun()

    return df