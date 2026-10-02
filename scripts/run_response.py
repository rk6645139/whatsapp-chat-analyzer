from src.parser import parse_whatsapp_chat
from src.preprocessing import preprocess_messages
from src.response_analysis import (
    calculate_response_times,
    get_average_response_time,
    get_median_response_time,
    get_fastest_response,
    get_slowest_response,
    get_response_time_by_user,
    get_response_matrix
)


df = parse_whatsapp_chat(
    "data/chat.txt"
)

df = preprocess_messages(df)

response_df = calculate_response_times(
    df,
    max_gap_minutes=60
)

print(
    "\nNumber of responses:",
    len(response_df)
)

print(
    "\nAverage response time:",
    round(
        get_average_response_time(response_df),
        2
    ),
    "minutes"
)

print(
    "Median response time:",
    round(
        get_median_response_time(response_df),
        2
    ),
    "minutes"
)

print(
    "Fastest response:",
    round(
        get_fastest_response(response_df),
        2
    ),
    "minutes"
)

print(
    "Slowest response:",
    round(
        get_slowest_response(response_df),
        2
    ),
    "minutes"
)

print("\nResponse time by user:")

print(
    get_response_time_by_user(
        response_df
    )
)

print("\nResponse matrix:")

print(
    get_response_matrix(
        response_df
    )
)