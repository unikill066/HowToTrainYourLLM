#!/usr/bin/env python3
"""
Unpack every WhatsApp “Export Chat” ZIP in a folder and save the embedded
.txt as <zip-name>.txt  (e.g.  WhatsApp Chat – Alice.zip ➜ WhatsApp Chat – Alice.txt)
"""

from pathlib import Path
import zipfile
import argparse
from typing import Union


def export_each_chat(directory: Union[str, Path]) -> None:
    root = Path(directory).expanduser().resolve()
    if not root.is_dir():
        raise FileNotFoundError(f"Folder does not exist: {root}")

    for zippath in sorted(root.glob("*.zip")):
        try:
            with zipfile.ZipFile(zippath) as z:
                txt_name = next(n for n in z.namelist() if n.lower().endswith(".txt"))
                chat_text = z.read(txt_name).decode("utf-8", errors="replace")
            dest_txt = zippath.with_suffix(".txt")  # same base-name as the zip
            dest_txt.write_text(chat_text, encoding="utf-8")
            print(f"Processed: {dest_txt.name}")

        except Exception as err:
            print(f"Exception:  {zippath.name}: {err}")


# # testing
# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="Extract WhatsApp chat .txt from each ZIP")
#     parser.add_argument("directory", help="Folder with WhatsApp *.zip files")
#     args = parser.parse_args()
#     export_each_chat(args.directory)