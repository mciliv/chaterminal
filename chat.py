#!/usr/bin/env python3

import os
import sys
import json
import requests
import argparse
from datetime import datetime
from pathlib import Path

import pyperclip


def new_message(chat, message) -> list[dict]:
    if chat.exists():
        with chat.open("r") as f:
            file_content = json.load(f)
        if isinstance(file_content, list):
            file_content.append(message)
    else:
        file_content = [message]
    with chat.open("w") as f:
        json.dump(file_content, f)
    return file_content


url = "https://api.openai.com/v1/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {os.environ["OPENAI_API_KEY"]}"
}


def chat(data):
    data = {
        "model": "gpt-4o",
        "messages": [{"role": "user", "content": data}],
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json().choices[0].message.content


def write(data, destination=Path.home()):
    filename = data[:16].replace(' ', '_') + str(datetime.now()) + '.md'
    with open(filename, 'w') as f:
        f.write(json.dumps(chat(data)))

if __name__ == "__main__":
    if sys.argv[1:] == '-p':
        write(pyperclip.paste())
    else:
        for path in sys.argv[1:]:
            path = Path(path)
            with open(path, 'r') as f:
                write(f.read(), path.parent)

