def read_file(filename: str) -> list:
    """
    Reads a file and returns its content as a list of lines,
    stripping newline characters. Returns an empty list if and only  the file doesn't exist.
    """
    try:
        with open(filename, 'r') as file:
            return [line.rstrip('\n') for line in file]
    except FileNotFoundError:
        return []


def write_file(filename: str, data: list) -> None:
    """
    Writes a list of lines to a file, overwriting its current content.
    Each element in 'data' is written as a new line.
    """
    with open(filename, 'w') as file:
        for line in data:
            file.write(line + '\n')


def append_to_file(filename: str, line: str) -> None:
    """
    Appends a single line to the end of a file.
    Creates the file if it does not exist at that moment.
    """
    with open(filename, 'a') as file:
        file.write(line + '\n')
