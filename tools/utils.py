import os
from typing import Literal, Dict, NoReturn, Callable, Any
from contextlib import contextmanager


def load_env_file(filename: str) -> Dict[str, str]:
    """Load environmental variables from a `.env` file."""
    result = {}
    with open(filename) as f:
        for line in f.readlines():
            if line.startswith('#') or not line.strip():
                # Skip this line. It's a comment or just whitespace.
                continue
            # Remove the end of line character
            line = line.rstrip()
            # Split the line into key and value
            key, value = line.split('=', 1)
            # Add the variable to the result
            result[key] = value
    return result


def yes_or_no(
        prompt: str,
        default: Literal['y', 'n'] = None,
        input_func: Callable[[str], str] = input,
        output_func: Callable[[str], Any] = print
):
    """Ask a yes/no question that returns True for "y/yes" and False for "n/no"."""
    if default not in ('y', 'n', None):
        raise ValueError("'The default value must be 'y' or 'n'.")

    while True:
        valid = ['y', 'n', 'yes', 'no']
        if not default:
            options_str = ' [y/n] '
        elif default == 'y':
            options_str = ' [Y/n] '
        else:
            options_str = ' [y/N] '
        response = input_func(prompt + options_str).strip().lower()
        if response not in valid:
            if default and response == '':
                return default == 'y'
            output_func("Please answer 'y' or 'n'.")
        else:
            return response.startswith('y')


def print_and_exit(msg: str, exit_code: int = 1) -> NoReturn:
    """Print a message and exit with the provided exit code."""
    print(msg)
    exit(exit_code)


@contextmanager
def using_dir(dir_new: str) -> None:
    """Temporarily change the working directory within a context manager."""
    dir_start = os.getcwd()
    try:
        os.chdir(dir_new)
        yield
    finally:
        os.chdir(dir_start)


if __name__ == '__main__':
    env = load_env_file('.env')
    print(env)
