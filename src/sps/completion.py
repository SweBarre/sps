import sys
import os


def get(cachefile, shell=None):
    """Generates a shell completion script

    Parameters
    ----------
    cachefile: str
        Path to cache file
    shell: str, optional
        Name of the shell to generate completion script for
        if not provided the function will try to use the 
        SHELL environment varable

    Raises
    ------
    SystemExit
        if an unknown shell is provided
        if shell is not provided and SHELL environ is not set
        if completion generation file is not readable
    """

    if shell == None:
        try:
            os.environ["SHELL"]
        except KeyError:
            print(
                "Error: Couldn't determin shell, you need to specify shell or set $SHELL environment variable",
                file=sys.stderr,
            )
            sys.exit(1)
        shell = os.path.basename(os.environ.get("SHELL"))
    if shell == "bash":
        filename = f"{os.path.dirname(os.path.realpath(__file__))}/completion.sh"
    else:
        print(f"Error: Unsupported shell specified '{shell}'", file=sys.stderr)
        sys.exit(1)

    try:
        with open(filename, "r") as f:  # pragma: no cover
            fc = f.read()
    except FileNotFoundError as err:
        print(f"Error: {err}", file=sys.stderr)
        sys.exit(2)
    fc = fc.replace("{sps_cachefile}", cachefile)
    return fc
