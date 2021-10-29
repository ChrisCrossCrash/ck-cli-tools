def load_env_file(filename: str = '.env') -> dict:
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


if __name__ == '__main__':
    env = load_env_file('.env')
    print(env)
