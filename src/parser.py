import re
from pathlib import Path

import pandas as pd


MESSAGE_PATTERN = re.compile(
    r"^\["
    r"(\d{1,2}/\d{1,2}/\d{2,4})"
    r",\s+"
    r"(\d{1,2}:\d{2}(?::\d{2})?\s*(?:AM|PM)?)"
    r"\]\s+"
    r"(.*?):\s"
    r"(.*)$",
    re.IGNORECASE
)


def parse_whatsapp_chat(file_path):

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"Chat file not found: {file_path}"
        )

    if file_path.suffix.lower() != ".txt":
        raise ValueError(
            "Please provide a WhatsApp .txt export file."
        )

    messages = []

    current_message = None

    with file_path.open(
        "r",
        encoding="utf-8-sig"
    ) as file:

        for raw_line in file:

            line = raw_line.rstrip(
                "\n\r"
            )

            match = MESSAGE_PATTERN.match(
                line
            )

            if match:

                if current_message is not None:

                    messages.append(
                        current_message
                    )

                date, time, sender, message = (
                    match.groups()
                )

                current_message = {
                    "date": date.strip(),
                    "time": time.strip(),
                    "sender": sender.strip(),
                    "message": message.strip()
                }

            else:

                if (
                    current_message is not None
                    and line.strip()
                ):

                    current_message[
                        "message"
                    ] += "\n" + line.strip()

    if current_message is not None:

        messages.append(
            current_message
        )

    if not messages:

        raise ValueError(
            "No WhatsApp messages were detected. "
            "Please upload a valid WhatsApp chat export."
        )

    return pd.DataFrame(
        messages
    )