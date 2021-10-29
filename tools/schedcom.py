#!/usr/bin/env python3

import argparse
import datetime
import re
import time
import subprocess

import ckcyberbot


def parse_args():
    parser = argparse.ArgumentParser(description='Schedule future tasks')
    parser.add_argument(
        'command',
        help='The command to be scheduled. Surround the command with quotation marks if it contains spaces.'
    )

    parser.add_argument(
        '-n',
        '--notify',
        help='Send a notification message via Telegram after the command is finished executing',
        action='store_true'
    )

    # `--at` and `--in` are mutually exclusive. They can't both be used in the same command.
    delay_options = parser.add_mutually_exclusive_group(required=True)
    delay_options.add_argument(
        '-a',
        '--at',
        help='time to start at. Format: YYYY-MM-DDTHH:MM:SS',
        metavar='STARTTIME'
    )
    delay_options.add_argument(
        '-i',
        '--in',
        dest='in_',
        metavar='DELAY',
        help='run the command after a delay. Example: "1d3h36m34s"'
    )

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()

    delay = 0

    if args.at:
        at_str: str = args.at
        at_datetime = None
        try:
            at_datetime = datetime.datetime.fromisoformat(at_str)
        except ValueError:
            print(f'Error: "{at_str}" is not a valid ISO 8601 date and time string.'
                  '\nVisit https://docs.python.org/3/library/datetime.html#datetime.datetime.isoformat'
                  ' for more information'
                  )
            exit(1)
        td = at_datetime - datetime.datetime.now()
        delay = td.total_seconds()
        if delay <= 0:
            print(f'Error: {at_datetime} is not a future time.')
            exit(2)

    else:
        in_str: str = args.in_

        match = re.match(r'^(?:(\d+)d)?(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?$', in_str)

        if not match:
            print(f'{in_str} is not a valid time delay.')
            exit(3)

        days, hours, minutes, seconds = match.groups()

        td = datetime.timedelta(
            days=int(days) if days else 0,
            hours=int(hours) if hours else 0,
            minutes=int(minutes) if minutes else 0,
            seconds=int(seconds) if seconds else 0
        )

        delay = td.total_seconds()

    delay = int(delay)

    print(f'Executing {args.command} in {delay} s.')
    time.sleep(delay)
    print(f'executing...')
    completed_process = subprocess.run(args.command, shell=True)

    # TODO: Display the output for the command in the Telegram message.
    if completed_process.returncode:
        success_msg = f'"{args.command}" did not run successfully.'
        print(success_msg)
        if args.notify:
            ckcyberbot.send_message(success_msg)
    else:
        fail_msg = f'"{args.command}" executed successfully!'
        print(fail_msg)
        if args.notify:
            ckcyberbot.send_message(fail_msg)
