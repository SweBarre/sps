import sys
import os


def get(cachefile, shell=None):
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
