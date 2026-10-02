# import streamlit as st
# import pandas as pd
# from wordcloud import WordCloud

# from src.parser import parse_whatsapp_chat
# from src.preprocessing import preprocess_messages

# from src.analytics import (
#     get_total_messages,
#     get_participant_count,
#     get_participants,
#     get_messages_per_user
# )

# from src.temporal import (
#     get_activity_summary,
#     get_daily_activity,
#     get_weekly_activity,
#     get_monthly_activity,
#     get_hourly_activity,
#     get_day_of_week_activity,
#     get_activity_heatmap
# )
# from src.analytics import (
#     get_total_messages,
#     get_participant_count,
#     get_participants,
#     get_messages_per_user,
#     get_user_statistics,
#     get_words_per_user
# )

# from src.nlp import (
#     get_word_frequency,
#     get_unique_word_count,
#     get_emoji_frequency,
#     get_total_emoji_count,
#     get_average_words_per_message,
#     get_longest_messages
# )

# # =====================================================
# # PAGE CONFIGURATION
# # =====================================================

# st.set_page_config(
#     page_title="WhatsApp Chat Analyzer",
#     page_icon="💬",
#     layout="wide"
# )


# # =====================================================
# # HEADER
# # =====================================================

# st.title(" WhatsApp Chat Analyzer")

# st.caption(
#     "NLP & Conversation Analytics Platform"
# )


# # =====================================================
# # FILE UPLOAD
# # =====================================================

# uploaded_file = st.file_uploader(
#     "Upload WhatsApp Chat Export",
#     type=["txt"]
# )


# # =====================================================
# # NO FILE UPLOADED
# # =====================================================

# if uploaded_file is None:

#     st.info(
#         "Upload a WhatsApp .txt chat export "
#         "to begin analysis."
#     )

#     st.stop()


# # =====================================================
# # SAVE TEMPORARY FILE
# # =====================================================

# temp_file = "data/temp_chat.txt"

# with open(
#     temp_file,
#     "wb"
# ) as file:

#     file.write(
#         uploaded_file.getbuffer()
#     )


# # =====================================================
# # PARSE CHAT
# # =====================================================

# try:

#     df = parse_whatsapp_chat(
#         temp_file
#     )

#     df = preprocess_messages(df)

# except Exception as error:

#     st.error(
#         f"Unable to process the chat: {error}"
#     )

#     st.stop()


# # =====================================================
# # EMPTY CHAT CHECK
# # =====================================================

# if df.empty:

#     st.warning(
#         "No messages were detected in this file."
#     )

#     st.stop()


# # =====================================================
# # BASIC ANALYTICS
# # =====================================================

# total_messages = (
#     get_total_messages(df)
# )

# participant_count = (
#     get_participant_count(df)
# )

# participants = (
#     get_participants(df)
# )

# messages_per_user = (
#     get_messages_per_user(df)
# )

# activity_summary = (
#     get_activity_summary(df)
# )


# # =====================================================
# # SIDEBAR
# # =====================================================

# st.sidebar.title("Navigation")

# st.sidebar.info(
#     "Dashboard modules will be added here."
# )


# # =====================================================
# # OVERVIEW
# # =====================================================

# st.header("Overview")


# # =====================================================
# # METRIC CARDS
# # =====================================================

# col1, col2, col3, col4 = st.columns(4)


# with col1:

#     st.metric(
#         "Total Messages",
#         total_messages
#     )


# with col2:

#     st.metric(
#         "Participants",
#         participant_count
#     )


# with col3:

#     st.metric(
#         "Most Active User",
#         messages_per_user.index[0]
#     )


# with col4:

#     st.metric(
#         "Active Hours",
#         activity_summary["active_hours"]
#     )


# # =====================================================
# # PARTICIPANTS
# # =====================================================

# st.subheader("👥 Participants")

# st.write(
#     ", ".join(participants)
# )


# # =====================================================
# # MESSAGES PER USER
# # =====================================================

# st.subheader(
#     "💬 Messages per Participant"
# )

# st.bar_chart(
#     messages_per_user
# )


# # =====================================================
# # ACTIVITY SUMMARY
# # =====================================================

# st.subheader(
#     "Activity Summary"
# )

# col1, col2 = st.columns(2)


# with col1:

#     st.write(
#         "Most active day"
#     )

#     st.info(
#         activity_summary[
#             "most_active_day"
#         ]
#     )


# with col2:

#     st.write(
#         "Most active hour"
#     )

#     st.info(
#         f"{activity_summary['most_active_hour']}:00"
#     )

#     # =====================================================
# # ACTIVITY ANALYSIS
# # =====================================================

# st.divider()

# st.header("📅 Activity Analysis")


# # =====================================================
# # DAILY ACTIVITY
# # =====================================================

# st.subheader("📈 Daily Message Activity")

# daily_activity = get_daily_activity(df)

# if not daily_activity.empty:

#     daily_chart = (
#         daily_activity
#         .set_index("date")["messages"]
#     )

#     st.line_chart(
#         daily_chart
#     )

# else:

#     st.info(
#         "No daily activity data available."
#     )


# # =====================================================
# # HOURLY ACTIVITY
# # =====================================================

# st.subheader("Messages by Hour")

# hourly_activity = get_hourly_activity(df)

# if not hourly_activity.empty:

#     hourly_chart = (
#         hourly_activity
#         .set_index("hour")["messages"]
#     )

#     st.bar_chart(
#         hourly_chart
#     )


# # =====================================================
# # DAY OF WEEK
# # =====================================================

# st.subheader("Messages by Day of Week")

# weekday_activity = (
#     get_day_of_week_activity(df)
# )

# if not weekday_activity.empty:

#     weekday_chart = (
#         weekday_activity
#         .set_index("day_of_week")["messages"]
#     )

#     st.bar_chart(
#         weekday_chart
#     )


# # =====================================================
# # WEEKLY ACTIVITY
# # =====================================================

# st.subheader("📊 Weekly Activity")

# weekly_activity = (
#     get_weekly_activity(df)
# )

# if not weekly_activity.empty:

#     weekly_chart = (
#         weekly_activity
#         .set_index("datetime")["messages"]
#     )

#     st.line_chart(
#         weekly_chart
#     )


# # =====================================================
# # MONTHLY ACTIVITY
# # =====================================================

# st.subheader("📅 Monthly Activity")

# monthly_activity = (
#     get_monthly_activity(df)
# )

# if not monthly_activity.empty:

#     monthly_chart = (
#         monthly_activity
#         .set_index("datetime")["messages"]
#     )

#     st.bar_chart(
#         monthly_chart
#     )

#     # =====================================================
# # ACTIVITY HEATMAP
# # =====================================================

# st.subheader(
#     "HOT: Activity Heatmap"
# )

# heatmap = get_activity_heatmap(df)

# if not heatmap.empty:

#     st.dataframe(
#         heatmap,
#         use_container_width=True
#     )

# else:

#     st.info(
#         "No heatmap data available."
#     )


# # =====================================================
# # PARTICIPANT ANALYSIS
# # =====================================================

# st.divider()

# st.header("Participant Analysis")


# # =====================================================
# # USER STATISTICS
# # =====================================================

# user_statistics = get_user_statistics(df)

# st.subheader("Participant Statistics")

# if not user_statistics.empty:

#     display_statistics = (
#         user_statistics
#         .copy()
#         .round(2)
#     )

#     st.dataframe(
#         display_statistics,
#         use_container_width=True
#     )

# else:

#     st.info(
#         "No participant statistics available."
#     )


# # =====================================================
# # MESSAGES PER PARTICIPANT
# # =====================================================

# st.subheader("Messages per Participant")

# if not messages_per_user.empty:

#     st.bar_chart(
#         messages_per_user
#     )


# # =====================================================
# # WORDS PER PARTICIPANT
# # =====================================================

# words_per_user = get_words_per_user(df)

# st.subheader("Words per Participant")

# if not words_per_user.empty:

#     st.bar_chart(
#         words_per_user
#     )

# # =====================================================
# # PARTICIPANT DETAIL
# # =====================================================

# st.subheader("Participant Detail")

# selected_user = st.selectbox(
#     "Select a participant",
#     ["All"] + participants
# )


# if selected_user != "All":

#     user_data = df[
#         df["sender"] == selected_user
#     ]

#     user_messages = len(user_data)

#     user_words = int(
#         user_data["word_count"].sum()
#     )

#     user_average_length = round(
#         user_data["character_count"].mean(),
#         2
#     )

#     user_media = int(
#         user_data["is_media"].sum()
#     )

#     user_links = int(
#         user_data["has_url"].sum()
#     )


#     # -------------------------
#     # Metrics
#     # -------------------------

#     col1, col2, col3, col4, col5 = st.columns(5)


#     with col1:

#         st.metric(
#             "Messages",
#             user_messages
#         )


#     with col2:

#         st.metric(
#             "Words",
#             user_words
#         )


#     with col3:

#         st.metric(
#             "Avg Message Length",
#             user_average_length
#         )


#     with col4:

#         st.metric(
#             "Media",
#             user_media
#         )


#     with col5:

#         st.metric(
#             "Links",
#             user_links
#         )


#     # -------------------------
#     # User activity
#     # -------------------------

#     st.subheader(
#         f"Activity: {selected_user}"
#     )

#     user_hourly = (
#         user_data
#         .groupby("hour")
#         .size()
#         .reindex(
#             range(24),
#             fill_value=0
#         )
#     )

#     st.line_chart(
#         user_hourly
#     )

# # =====================================================
# # NLP ANALYSIS
# # =====================================================

# st.divider()

# st.header("NLP Analysis")


# # =====================================================
# # NLP METRICS
# # =====================================================

# total_unique_words = get_unique_word_count(df)

# average_words = get_average_words_per_message(df)

# total_emojis = get_total_emoji_count(df)


# col1, col2, col3 = st.columns(3)


# with col1:

#     st.metric(
#         "Unique Words",
#         total_unique_words
#     )


# with col2:

#     st.metric(
#         "Average Words per Message",
#         round(average_words, 2)
#     )


# with col3:

#     st.metric(
#         "Total Emojis",
#         total_emojis
#     )


# # =====================================================
# # WORD FREQUENCY
# # =====================================================

# st.subheader("Most Frequent Words")

# word_frequency = get_word_frequency(
#     df,
#     top_n=20
# )

# # =====================================================
# # WORDCLOUD
# # =====================================================
# st.subheader("WordCloud")

# if word_frequency:
#     word_counts = dict(word_frequency)

#     wordcloud = WordCloud(
#         width=1400,
#         height=500,
#         background_color="white",
#         max_words=100,
#         collocations=False
#     ).generate_from_frequencies(word_counts)

#     st.image(
#         wordcloud.to_array(),
#         use_container_width=True
#     )
# else:
#     st.info("Not enough text to generate a WordCloud.")



# if word_frequency:

#     word_df = (
#         __import__("pandas")
#         .DataFrame(
#             word_frequency,
#             columns=[
#                 "word",
#                 "frequency"
#             ]
#         )
#         .set_index("word")
#     )

#     st.bar_chart(
#         word_df
#     )

# else:

#     st.info(
#         "No word frequency data available."
#     )


# # =====================================================
# # EMOJI FREQUENCY
# # =====================================================

# st.subheader("Most Used Emojis")

# emoji_frequency = get_emoji_frequency(
#     df,
#     top_n=20
# )


# if emoji_frequency:

#     emoji_df = pd.DataFrame(
#     emoji_frequency,
#     columns=["emoji", "frequency"]
# ).set_index("emoji")

#     st.bar_chart(
#         emoji_df
#     )

# else:

#     st.info(
#         "No emojis found in this conversation."
#     )


# # =====================================================
# # LONGEST MESSAGES
# # =====================================================

# st.subheader("Longest Messages")

# longest_messages = get_longest_messages(
#     df,
#     top_n=10
# )


# if not longest_messages.empty:

#     st.dataframe(
#         longest_messages,
#         use_container_width=True
#     )


# # =====================================================
# # PARTICIPANT NLP
# # =====================================================

# st.subheader(
#     "Participant NLP Analysis"
# )


# nlp_user = st.selectbox(
#     "Select participant for NLP analysis",
#     ["All"] + participants,
#     key="nlp_user"
# )


# if nlp_user == "All":

#     nlp_data = df

# else:

#     nlp_data = df[
#         df["sender"] == nlp_user
#     ]


# user_word_frequency = get_word_frequency(
#     nlp_data,
#     top_n=15
# )


# if user_word_frequency:

#     user_word_df = (
#         __import__("pandas")
#         .DataFrame(
#             user_word_frequency,
#             columns=[
#                 "word",
#                 "frequency"
#             ]
#         )
#         .set_index("word")
#     )

#     st.bar_chart(
#         user_word_df
#     )

# else:

#     st.info(
#         "No NLP data available for this participant."
#     )

import streamlit as st

from src.ui import render_sidebar


st.set_page_config(
    page_title="WhatsApp Chat Analyzer",
    page_icon="💬",
    layout="wide"
)


# --------------------------------
# Load chat once
# --------------------------------

df = render_sidebar()


# --------------------------------
# Navigation
# --------------------------------

if df is None:

    navigation = st.navigation(
        [
            st.Page(
                "views/00_Home.py",
                title="Home",
                icon=":material/home:"
            )
        ]
    )

else:

    navigation = st.navigation(
        {
            "Analysis": [

                st.Page(
                    "views/01_Overview.py",
                    title="Overview",
                    icon=":material/dashboard:"
                ),

                st.Page(
                    "views/02_Participants.py",
                    title="Participants",
                    icon=":material/group:"
                ),

                st.Page(
                    "views/03_Activity.py",
                    title="Activity",
                    icon=":material/analytics:"
                ),

                st.Page(
                    "views/04_NLP.py",
                    title="NLP",
                    icon=":material/text_fields:"
                ),

                st.Page(
                    "views/05_Sentiment.py",
                    title="Sentiment",
                    icon=":material/mood:"
                ),

                st.Page(
                    "views/06_Toxicity.py",
                    title="Toxicity",
                    icon=":material/security:"
                ),

                st.Page(
                    "views/07_Topics.py",
                    title="Topics",
                    icon=":material/topic:"
                ),

                st.Page(
                    "views/08_Response_Analysis.py",
                    title="Response Analysis",
                    icon=":material/schedule:"
                ),

                st.Page(
                    "views/09_Search.py",
                    title="Search",
                    icon=":material/search:"
                ),

                st.Page(
                    "views/10_Summary.py",
                    title="Summary",
                    icon=":material/summarize:"
                ),
            ]
        }
    )


navigation.run()