import sys
from pathlib import Path
from argparse import ArgumentParser
from prettytable import PrettyTable
from sps import products, packages, completion, __version__


def create_parser(args=sys.argv[1:]):
    """Create a argparse.ArgumentParser

    Creates a ArgumentParser based on command line

    Parameters
    ----------
    args: list, optional
        a list that represents how it was called from the command line
        if not specified the list is build wid sys.argv[1:]

    Returns
    -------
    argparse.ArgumentParser
    """


    parser = ArgumentParser()
    for opt in ["-C", "--cache-file"]:
        try:
            i = args.index(opt)
            args.pop(i + 1)
            args.pop(i)
        except ValueError:
            pass
    args = [arg for arg in args if not arg.startswith("-")]
    parser.add_argument(
        "--cache-file",
        "-C",
        help=f"cache file to use, (default: { str(Path.home()) }/.cache/sps_cache.json",
        default=f"{ str(Path.home()) }/.cache/sps_products.json",
    )
    parser.add_argument(
        "--version", "-v", action="version", version=f"%(prog)s {__version__}"
    )
    if not args:
        parser.add_argument(
            "command",
            help="command to run",
            choices=["package", "product", "completion"],
        )
        parser.add_argument("pattern", nargs="?", help="pattern to search for")

    if args:
        if args[0] == "product":
            parser.add_argument("command", help="product related tasks")
            parser.add_argument("pattern", nargs="?", help="pattern to search for")
            parser.add_argument(
                "--update-cache",
                "-u",
                help="Update the local product cache",
                action="store_true",
            )
            parser.add_argument(
                "--no-cache",
                "-N",
                help="Don't use the local cache",
                action="store_true",
            )
            parser.add_argument(
                "--short",
                "-s",
                help="Just print product identifier",
                action="store_true",
            )
            parser.add_argument(
                "--sort-table",
                "-S",
                help="Sort output by column",
                choices=["id", "Name", "Edition", "Identifier", "Arch"],
                default="id",
            )
        if args[0] == "package":
            parser.add_argument("command", help="package related tasks")
            parser.add_argument(
                "product", help="product id or identifier to search for packages in"
            )
            parser.add_argument("pattern", nargs="?", help="pattern to search for")
            parser.add_argument(
                "--exact-match",
                "-e",
                help="Only show where PATTERN matches exact",
                action="store_true",
            )
            parser.add_argument(
                "--sort-table",
                "-S",
                help="Sort output by column",
                choices=["Name", "Version", "Release", "Arch", "Module"],
                default="Name",
            )
        if args[0] in ["product", "package"]:
            parser.add_argument(
                "--no-borders", "-n", help="Do not print borders", action="store_true"
            )
            parser.add_argument(
                "--no-header", "-H", help="Do not print headers", action="store_true"
            )
        if args[0] == "completion":
            parser.add_argument("command", help="tab completion raleated tasks")
            parser.add_argument(
                "shell",
                nargs="?",
                help="shell to generate tab completion for (defaults ti $SHELL",
                choices=["bash"],
            )

    return parser


def main():
    """The main program logic"""


    parser = create_parser()
    args = parser.parse_args()

    if args.command in ["product", "package"]:
        table = PrettyTable()
        if args.command == "product":
            products_data = products.get(
                args.pattern, args.cache_file, args.no_cache, args.update_cache
            )
            table.field_names = ["id", "Name", "Edition", "Identifier", "Arch"]
            for name in table.field_names:
                table.align[name] = "l"
            for product in products_data:
                table.add_row(
                    [
                        product["id"],
                        product["name"],
                        product["edition"],
                        product["identifier"],
                        product["architecture"],
                    ]
                )
            if args.short:
                table.border = False
                table.header = False
                print(table.get_string(fields=["Identifier"]))
                return

        if args.command == "package":
            package_data = packages.get(args.product, args.pattern, args.cache_file)
            table.field_names = ["Name", "Version", "Release", "Arch", "Module"]
            for name in table.field_names:
                table.align[name] = "l"
            for package in package_data:
                module_line = ""
                for product in package["products"]:
                    module_line = "{},{}".format(module_line, product["name"])
                if args.exact_match and package["name"] == args.pattern:
                    table.add_row(
                        [
                            package["name"],
                            package["version"],
                            package["release"],
                            package["arch"],
                            module_line[1:],
                        ]
                    )
                elif not args.exact_match:
                    table.add_row(
                        [
                            package["name"],
                            package["version"],
                            package["release"],
                            package["arch"],
                            module_line[1:],
                        ]
                    )
        table.border = not args.no_borders
        table.header = not args.no_header
        table.sortby = args.sort_table
        print(table)
    if args.command == "completion":
        print(completion.get(args.cache_file, args.shell))
