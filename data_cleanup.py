# imports
from constants import *
from pathlib import Path
from src.utils.data_extraction_whatsapp import export_each_chat
from src.utils.whatsapp_message_pre_processing import read_whatsapp_chat

all_chats = dict()
export_each_chat(CHAT_DATA_DIR)

for file in CHAT_DATA_DIR.glob('*.txt'):
    file_name = file.stem
    all_chats[file_name] = read_whatsapp_chat(file)

text_sequence = ""
for file_name in all_chats.keys():
    text_sequence += " ".join(all_chats[file_name]['message'].values)

with open(DATA_DIR / "whatsapp_text.txt", "w", encoding="utf-8") as f:
    f.write(text_sequence)

print(len(text_sequence))