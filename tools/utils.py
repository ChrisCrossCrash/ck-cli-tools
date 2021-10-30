from typing import Literal, Dict


def load_env_file(filename: str) -> Dict[str, str]:
    """Load environmental variables from a `.env` file."""
    result = {}
    with open(filename) as f:
        for line in f.readlines():
            if line.startswith('#'):
                # Skip this line. It's a comment.
                continue
            # Remove the end of line character
            line = line.rstrip()
            # Split the line into key and value
            key, value = line.split('=', 1)
            # Add the variable to the result
            result[key] = value
    return result


def yes_or_no(prompt: str, default: Literal['y', 'n'] = None):
    """Ask a yes/no question that returns True for "y/yes" and False for "n/no"."""
    while True:
        valid = ['y', 'n', 'yes', 'no']
        if not default:
            options_str = ' [y/n] '
        elif default == 'y':
            options_str = ' [Y/n] '
        else:
            options_str = ' [y/N] '
        response = input(prompt + options_str).strip().lower()
        if response not in valid:
            print("Please answer 'y' or 'n'.")
        else:
            return response.startswith('y')


if __name__ == '__main__':
    env = load_env_file('.env')
    print(env)
