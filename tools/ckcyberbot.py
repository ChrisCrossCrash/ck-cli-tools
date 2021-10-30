import json
from urllib.request import urlopen
from urllib.request import Request
from utils import load_env_file
import os


# Telegram Bot API Documentation
# https://core.telegram.org/bots/api


class Bot:
    def __init__(self, token, chat_id):
        self.token = token
        self.chat_id = chat_id

    def get_url(self, method_str: str) -> str:
        return f'https://api.telegram.org/bot{self.token}/{method_str}'

    def get_me(self):
        with urlopen(self.get_url('getMe')) as response:
            return json.load(response)

    def get_updates(self):
        with urlopen(self.get_url('getUpdates')) as response:
            return json.load(response)

    def send_message(self, text: str):
        post_data = {
            'chat_id': self.chat_id,
            'text': text,
            # https://core.telegram.org/bots/api#html-style
            # 'parse_mode': 'HTML'
        }

        post_data_encoded = json.dumps(post_data).encode('ascii')

        request = Request(
            self.get_url('sendMessage'),
            post_data_encoded,
            {'Content-Type': 'application/json'},
        )

        with urlopen(request) as response:
            return response


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    from pprint import pprint

    env = load_env_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env'))
    TELEGRAM_TOKEN = env['TELEGRAM_TOKEN']
    TELEGRAM_CHAT_ID = env['TELEGRAM_CHAT_ID']

    bot = Bot(TELEGRAM_TOKEN, TELEGRAM_CHAT_ID)

    # To get info about the bot:
    # pprint(bot.get_me())

    # To get a chat_id, first send a message to the bot,
    # then get the chat_id using get_updates()
    # pprint(bot.get_updates())

    message_text = 'Hi'
    result = bot.send_message(message_text)
    print(result)
