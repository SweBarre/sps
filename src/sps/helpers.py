import sys

# Color codes
CRESET = "\x1b[0m"
CWARNING = "\x1b[0;30;43m"
CERROR = "\x1b[0;37;41m"


def print_warn(message):
    """Print formated message to stderr

    Parameters
    ----------
    message: str
    """

    print(f"{CWARNING}Warning:{CRESET} {message}", file=sys.stderr)


def print_err(message):
    """Print formated message to stderr

    Parameters
    ----------
    message: str
    """

    print(f"{CERROR}Error:{CRESET} {message}", file=sys.stderr)


def line_format(data, length=75, indent=0):
    """Format the input to a max row length

    Parameters
    ----------
    data: list
        list och items that is beeing formated
    length: int
        how long is the max row length
    indent: int
        how many whitespaces should each line start with

    Returns
    ------
    str
    """

    returnstring = ""
    row = "" + (" " * indent)
    for i in data:
        if len(row + i) > length or len(i) >= length:
            returnstring += row + i + "\n"
            row = "" + (" " * indent)
        else:
            row += i + " "
    returnstring += row + "\n"
    return returnstring.rstrip()
