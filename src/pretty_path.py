import os
import argparse
import re
import sys


def pretty_path(search_pattern=None, ignore_pattern=None):
    # folders = os.environ['PATH'].split(';')
    folders = re.split(r'[;:]', os.environ['PATH'])

    if search_pattern:
        pattern = re.compile(search_pattern, re.IGNORECASE if sys.platform == 'win32' else 0)
        folders = [folder for folder in folders if pattern.search(folder)]

    if ignore_pattern:
        pattern = re.compile(ignore_pattern, re.IGNORECASE if sys.platform == 'win32' else 0)
        folders = [folder for folder in folders if not pattern.search(folder)]

    for folder in folders:
        if folder:
            print(folder)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Print the `PATH` variable in a human-readable way.')
    parser.add_argument('--search', help='Only show path directories matching this pattern')
    parser.add_argument('--ignore', help='Ignore path directories matching this pattern')
    args = parser.parse_args()
    pretty_path(search_pattern=args.search, ignore_pattern=args.ignore)
