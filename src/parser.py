# import re
# from pathlib import Path

# import pandas as pd


# MESSAGE_PATTERN = re.compile(
#     r"^\["
#     r"(\d{1,2}/\d{1,2}/\d{2,4})"
#     r",\s+"
#     r"(\d{1,2}:\d{2}(?::\d{2})?\s*(?:AM|PM)?)"
#     r"\]\s+"
#     r"(.*?):\s"
#     r"(.*)$",
#     re.IGNORECASE
# )


# def parse_whatsapp_chat(file_path):

#     file_path = Path(file_path)

#     if not file_path.exists():
#         raise FileNotFoundError(
#             f"Chat file not found: {file_path}"
#         )

#     if file_path.suffix.lower() != ".txt":
#         raise ValueError(
#             "Please provide a WhatsApp .txt export file."
#         )

#     messages = []

#     current_message = None

#     with file_path.open(
#         "r",
#         encoding="utf-8-sig"
#     ) as file:

#         for raw_line in file:

#             line = raw_line.rstrip(
#                 "\n\r"
#             )

#             match = MESSAGE_PATTERN.match(
#                 line
#             )

#             if match:

#                 if current_message is not None:

#                     messages.append(
#                         current_message
#                     )

#                 date, time, sender, message = (
#                     match.groups()
#                 )

#                 current_message = {
#                     "date": date.strip(),
#                     "time": time.strip(),
#                     "sender": sender.strip(),
#                     "message": message.strip()
#                 }

#             else:

#                 if (
#                     current_message is not None
#                     and line.strip()
#                 ):

#                     current_message[
#                         "message"
#                     ] += "\n" + line.strip()

#     if current_message is not None:

#         messages.append(
#             current_message
#         )

#     if not messages:

#         raise ValueError(
#             "No WhatsApp messages were detected. "
#             "Please upload a valid WhatsApp chat export."
#         )

#     return pd.DataFrame(
#         messages
#     )

import re
from pathlib import Path

import pandas as pd


# Example:
# 01/06/2026, 09:49 - Varun S KGI: Jaldi aao
HYPHEN_MESSAGE_PATTERN = re.compile(
    r"^(\d{1,2}/\d{1,2}/\d{2,4}),\s+"
    r"(\d{1,2}:\d{2}(?::\d{2})?(?:\s*[APMapm]{2})?)\s+-\s+"
    r"(.+?):\s(.*)$"
)

# Example:
# [01/09/26, 10:00:00 AM] Alice: Hello
BRACKET_MESSAGE_PATTERN = re.compile(
    r"^\[(\d{1,2}/\d{1,2}/\d{2,4}),\s+"
    r"(\d{1,2}:\d{2}(?::\d{2})?(?:\s*[APMapm]{2})?)\]\s+"
    r"(.+?):\s(.*)$"
)


def _read_chat_file(file_path):
    """Read a WhatsApp export using common encodings."""

    encodings = [
        "utf-8-sig",
        "utf-8",
        "utf-16",
        "utf-16-le",
        "utf-16-be",
        "cp1252",
    ]

    for encoding in encodings:
        try:
            with open(file_path, "r", encoding=encoding) as file:
                content = file.read()

            # Avoid accepting incorrectly decoded UTF-16 content.
            if "\x00" in content:
                continue

            return content

        except (UnicodeDecodeError, UnicodeError):
            continue

    raise ValueError(
        "Unable to decode the WhatsApp export file. "
        "The file may use an unsupported encoding."
    )


def parse_whatsapp_chat(file_path):
    """Parse WhatsApp exported chat text."""

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"Chat file not found: {file_path}"
        )

    if file_path.suffix.lower() != ".txt":
        raise ValueError(
            "Please provide a WhatsApp .txt export file."
        )

    content = _read_chat_file(file_path)

    messages = []
    current_message = None

    for raw_line in content.splitlines():

        line = raw_line.strip()

        if not line:
            continue

        match = HYPHEN_MESSAGE_PATTERN.match(line)

        if not match:
            match = BRACKET_MESSAGE_PATTERN.match(line)

        if match:

            if current_message is not None:
                messages.append(current_message)

            date, time, sender, message = match.groups()

            current_message = {
                "date": date.strip(),
                "time": time.strip(),
                "sender": sender.strip(),
                "message": message.strip(),
            }

        else:

            # Ignore timestamped system messages.
            #
            # Example:
            # 23/12/2025, 15:52 - Messages and calls are end-to-end encrypted...
            #
            # These do not contain "sender: message".

            system_message = re.match(
                r"^\[?\d{1,2}/\d{1,2}/\d{2,4},\s+"
                r"\d{1,2}:\d{2}(?::\d{2})?"
                r"(?:\s*[APMapm]{2})?"
                r"\]?\s+-\s+",
                line,
            )

            if system_message:

                if current_message is not None:
                    messages.append(current_message)
                    current_message = None

                continue

            # Multiline message
            if current_message is not None:
                current_message["message"] += "\n" + line

    if current_message is not None:
        messages.append(current_message)

    if not messages:
        raise ValueError(
            "No WhatsApp messages were detected. "
            "Please upload a valid WhatsApp chat export."
        )

    return pd.DataFrame(messages)