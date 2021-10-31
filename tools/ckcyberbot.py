#!/usr/bin/env python3

import json
from urllib.request import urlopen, Request
import argparse
from typing import Dict
from secrets import randbelow
from http.client import HTTPResponse

from utils import load_env_file, yes_or_no
from exceptions import ChatIdMissingError


# Telegram Bot API Documentation
# https://core.telegram.org/bots/api


class Bot:
    def __init__(self, token: str, chat_id: str = None):
        self.token = token
        self.chat_id = chat_id

    def get_url(self, method_str: str) -> str:
        return f'https://api.telegram.org/bot{self.token}/{method_str}'

    def get_me(self) -> dict:
        with urlopen(self.get_url('getMe')) as response:
            return json.load(response)

    def get_updates(self) -> dict:
        with urlopen(self.get_url('getUpdates')) as response:
            return json.load(response)

    def send_message(self, text: str) -> HTTPResponse:
        if not self.chat_id:
            raise ChatIdMissingError

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
    parser = argparse.ArgumentParser(
        description='Generate a .env file with the required variables to use `ckcyberbot`'
                    ' in other modules. If a `.env` file already exists and does not'
                    ' already contain the required variables, append to it.'
    )
    # TODO: Make the token argument optional if the user alread has it in a .env file
    parser.add_argument(
        'token',
        help='your Telegram bot\'s unique token https://core.telegram.org/bots/api#authorizing-your-bot'
    )
    # TODO: Make it possible to overwrite an existing (invalid) chat ID.
    parser.add_argument(
        '-c',
        '--chat-id',
        help='the chat id you want your bot to send notifications to, if it exists'
    )
    args = parser.parse_args()

    bot = Bot(args.token, args.chat_id)

    # Create a chat_id if it wasn't specified.
    if not bot.chat_id:
        sec_code = str(randbelow(10000)).zfill(4)
        input(f'Send the code "{sec_code}" to your bot via Telegram message and then press Enter.')
        updates: dict = bot.get_updates()
        # FIXME: This throws IndexError after the first attempt after creating a new chat.
        sec_code_from_update = updates['result'][-1]['message']['text']
        if sec_code_from_update == sec_code:
            bot.chat_id = updates['result'][-1]['message']['chat']['id']
        else:
            print('The security code didn\'t match.')
            exit(1)

    # Send a test message.
    test_msg_code = str(randbelow(10000)).zfill(4)
    test_msg = f'Test messsage: {test_msg_code}'
    bot.send_message(test_msg)
    sent_code = yes_or_no(f'Did the bot just send you the code {test_msg_code}')

    if not sent_code:
        print('Bot code didn\'t match. Exiting...')
        exit(2)

    # create or append to the .env file
    env: Dict[str, str] = {
        'TELEGRAM_TOKEN': '',
        'TELEGRAM_CHAT_ID': '',
    }
    is_updating_existing_file = True
    try:
        env.update(load_env_file('.env'))
        print('Existing .env file found. Updating with Telegram varaibles...')
    except FileNotFoundError:
        is_updating_existing_file = False
        print('Existing .env file not found. Creating new .env file...')

    with open('.env', 'a') as file:
        if not env['TELEGRAM_TOKEN']:
            file.write(f'TELEGRAM_TOKEN={bot.token}\n')
        if not env['TELEGRAM_CHAT_ID']:
            file.write(f'TELEGRAM_CHAT_ID={bot.chat_id}\n')

    if is_updating_existing_file:
        print('Successfully updated .env file!')
    else:
        print('Successfully created new .env file!')
