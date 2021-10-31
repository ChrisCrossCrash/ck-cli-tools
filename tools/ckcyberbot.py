#!/usr/bin/env python3

import json
from urllib.request import urlopen, Request
import argparse
from typing import Dict, List
from secrets import randbelow
from http.client import HTTPResponse
import re

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

    def get_updates(
            self,
            limit: int = 100,
            allowed_updates: List[str] = None,
            timeout: int = 0,
            offset: int = 0
    ) -> dict:
        if not allowed_updates:
            allowed_updates = []

        post_data = {
            'limit': limit,
            'allowed_updates': allowed_updates,
            'timeout': timeout,
            'offset': offset,
        }

        post_data_encoded = json.dumps(post_data).encode('ascii')

        request = Request(
            self.get_url('getUpdates'),
            post_data_encoded,
            {'Content-Type': 'application/json'},
        )

        with urlopen(request) as response:
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
    chat_id_options = parser.add_mutually_exclusive_group()
    chat_id_options.add_argument(
        '-c',
        '--chat-id',
        help='the chat ID you want your bot to send notifications to, if it exists'
    )
    chat_id_options.add_argument(
        '--new-chat-id',
        help='force the creation of a new `TELEGRAM_CHAT_ID` variable if one already exists.'
             ' This can be helpful if the existing chat ID is invalid.',
        action='store_true'
    )
    args = parser.parse_args()

    bot = Bot(args.token, args.chat_id)

    # Create a chat_id if it wasn't specified or if the `--new-chat-id` option was used.
    if not bot.chat_id or args.new_chat_id:
        sec_code = str(randbelow(10000)).zfill(4)
        input(f'Send the code "{sec_code}" to your bot via Telegram message and then press Enter.')
        updates: dict = bot.get_updates(
            limit=1,
            allowed_updates=['message'],
            offset=-1
        )
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

    with open('.env', 'r+') as file:
        if not env['TELEGRAM_TOKEN']:
            file.write(f'TELEGRAM_TOKEN={bot.token}\n')
        if not env['TELEGRAM_CHAT_ID']:
            file.write(f'TELEGRAM_CHAT_ID={bot.chat_id}\n')
        else:
            # Replace the existing TELGRAM_CHAT_ID in the file
            old_content = file.read()
            updated_content = re.sub(
                r'(?!TELEGRAM_CHAT_ID=)\d+',
                str(bot.chat_id),
                old_content,
                flags=re.MULTILINE
            )
            file.seek(0)
            file.write(updated_content)
            file.truncate()

    if is_updating_existing_file:
        print('Successfully updated .env file!')
    else:
        print('Successfully created new .env file!')
