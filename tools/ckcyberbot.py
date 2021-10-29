"""
# How to make Telegram API requests
# https://core.telegram.org/bots/api#making-requests

For this to work, you'll need to create a `.env` file in the same directory
as this module with the variables TELEGRAM_TOKEN and TELEGRAM_CHAT_ID.
"""

import json
from urllib.request import urlopen
from urllib.request import Request
from utils import load_env_file

env = load_env_file()
TELEGRAM_TOKEN = env['TELEGRAM_TOKEN']
TELEGRAM_CHAT_ID = env['TELEGRAM_CHAT_ID']


def get_url(method_str: str) -> str:
    return f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/{method_str}'


def get_me():
    with urlopen(get_url('getMe')) as response:
        return json.load(response)


def get_updates():
    with urlopen(get_url('getUpdates')) as response:
        return json.load(response)


def send_message(text: str):
    post_data = {
        'chat_id': env['TELEGRAM_CHAT_ID'],
        'text': text,
        # FIXME: Find out why MarkdownV2 gives 400 Not Found errors.
        # 'parse_mode': 'MarkdownV2'
    }

    post_data = json.dumps(post_data).encode('ascii')

    request = Request(
        get_url('sendMessage'),
        post_data,
        {'Content-Type': 'application/json'},
    )

    with urlopen(request) as response:
        return response


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    from pprint import pprint

    # To get info about the bot:
    # pprint(get_me())

    # To get a chat_id, first send a message to the bot,
    # then get the chat_id using get_updates()
    # pprint(get_updates())

    message_text = 'Hi'
    result = send_message(message_text)
    print(result)
