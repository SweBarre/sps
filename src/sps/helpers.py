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
