import re
import pandas as pd


def read_whatsapp_chat(file_path: str) -> pd.DataFrame:
    # Define filtering patterns
    encryption_message = "Messages and calls are end-to-end encrypted. No one outside of this chat, not even WhatsApp, can read or listen to them. Tap to learn more."
    media_pattern = "<Media omitted>"
    email_pattern = r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}'
    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    edited_message = "<This message was edited>"
    deleted_message = "You deleted this message"
    null_message = "null"
    created_group_message = "created group"
    added_you_to_group_message = "added you"
    tagging_pattern = r'@[\w]+'

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Apply filters to remove unwanted lines
    filtered_lines = []
    for line in lines:
        if (
            encryption_message not in line and
            deleted_message not in line and
            null_message != line.split(" ")[-1] and
            media_pattern not in line and
            created_group_message not in line and
            added_you_to_group_message not in line and
            not re.search(email_pattern, line) and
            not re.search(url_pattern, line)
        ):
            line = line.replace(edited_message, "").strip()
            line = re.sub(tagging_pattern, "", line).strip()
            filtered_lines.append(line)

    # Normalize content:
    content = '\n'.join(filtered_lines)
    # Replace narrow no-break space (iOS specific)
    content = content.replace('\u202f', ' ')
    # Remove square brackets if they surround the timestamp (only for iOS)
    content = re.sub(
        r'\[(\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{2}(?::\d{2})?\s?[APap][Mm])\]',
        r'\1',
        content
    )
    # Remove LRM and RLM characters (Left-to-Right Mark and Right-to-Left Mark)
    content = content.replace('\u200E', '').replace('\u200F', '')

    # Updated regex pattern to match both iOS and Android WhatsApp exports.
    pattern = r'(\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{2}(?::\d{2})?(?:\s?[APap][Mm])?)\s?(?:-|\~)?\s?(.*?): (.*?)(?=\n\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{2}|$)'
    messages = re.findall(pattern, content, re.DOTALL)
    df = pd.DataFrame(messages, columns=['timestamp', 'sender', 'message'])

    timestamps = []
    for timestamp in df['timestamp']:
        try:
            timestamp = pd.to_datetime(
                timestamp, format='mixed', errors='coerce')
        except Exception as e:
            print(f"Error parsing timestamp '{timestamp}': {e}")
            timestamp = pd.NaT
        timestamps.append(timestamp)

    df['timestamp'] = timestamps
    return df


# read_whatsapp_chat("/Users/discovery/Desktop/httallm/data/all_chats.txt").to_csv("/Users/discovery/Desktop/httallm/data/all_chats.csv", index=False)