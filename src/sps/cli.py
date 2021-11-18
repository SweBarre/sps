import sys
from pathlib import Path
from argparse import ArgumentParser
from prettytable import PrettyTable, ALL
from sps import cache, products, packages, completion, patchproducts
from sps import patch, __version__
from sps.helpers import print_warn


PATCH_WARN_NUMBER = 500


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
    for opt in ["-C", "--cache-file", "-a", "--cache-age"]:
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
        help=f"cache file to use, (default: $HOME/.cache/sps_cache.json",
        default=f"{ str(Path.home()) }/.cache/sps_cache.json",
    )
    parser.add_argument(
        "--cache-age",
        "-a",
        help="Number of days before cache entry is flagged as old",
        type=int,
        default=60,
    )
    parser.add_argument(
        "--version", "-v", action="version", version=f"%(prog)s {__version__}"
    )
    if not args:
        parser.add_argument(
            "command",
            help="command to run",
            choices=["package", "product", "completion", "patchproduct"],
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
        if args[0] == "patchproduct":
            parser.add_argument("command", help="Patch product related tasks")
            parser.add_argument("pattern", nargs="?", help="pattern to search for")
            parser.add_argument(
                "--no-cache",
                "-N",
                help="Don't use the local cache",
                action="store_true",
            )
            parser.add_argument(
                "--update-cache",
                "-u",
                help="Update the local patch product cache",
                action="store_true",
            )
            parser.add_argument(
                "--sort-table",
                "-S",
                help="Sort output by column",
                choices=["Name", "Version", "Arch", "id"],
                default="Name",
            )
        if args[0] == "patch":
            parser.add_argument("command", help="Patch related tasts")
            parser.add_argument(
                "pattern", nargs="?", help="search by CVE, patch name, keywords"
            )
            parser.add_argument(
                "--severity",
                "-e",
                help="search for patches with this severity level",
                choices=["all", "low", "moderate", "important", "critical"],
                default="all",
            )
            parser.add_argument(
                "--only-security-patches",
                "-o",
                help="only search for security patches",
                action="store_true",
            )
            parser.add_argument(
                "--date-from",
                "-f",
                help="search for patches starting from date YYYY-m-d (2020-6-29)",
            )
            parser.add_argument(
                "--date-to",
                "-t",
                help="search for patches ending at date YYYY-m-d (2020-6-29)",
            )
            parser.add_argument(
                "--page",
                "-p",
                help="page number in search result to display",
                type=int,
                default=1,
            )
            parser.add_argument(
                "--sort-table",
                "-S",
                help="Sort output by column",
                choices=["Severity", "Name", "Product", "Arch", "id", "Released"],
                default="Released",
            )
            parser.add_argument(
                "--product",
                "-P",
                help="Product to limit the search to, spaces in product name replaced with underscore",
            )
            parser.add_argument(
                "--arch", "-A", help="Architecture to limit the search to"
            )
            parser.add_argument(
                "--product-version",
                "-V",
                help="Version to limit the search to, spaces replaced with underscore",
            )
            parser.add_argument(
                "--detail",
                "-d",
                help="Show detailed patch information",
                action="store_true",
            )

        if args[0] in ["product", "package", "patchproduct", "patch"]:
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

    if args.command in ["product", "package", "patchproduct", "patch"]:
        table = PrettyTable()
        if args.command == "product":
            products_data = products.get(
                args.pattern, args.cache_file, args.no_cache, args.update_cache
            )
            table.field_names = ["id", "Name", "Edition", "Identifier", "Arch"]
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

        if args.command == "package":
            package_data = packages.get(args.product, args.pattern, args.cache_file)
            table.field_names = ["Name", "Version", "Release", "Arch", "Module"]
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
        if args.command == "patchproduct":
            products_data = patchproducts.get(
                args.pattern, args.cache_file, args.no_cache, args.update_cache
            )
            table.field_names = ["Name", "Version", "Arch"]
            for product in products_data:
                table.add_row(
                    [
                        product["name"],
                        product["version"],
                        product["architecture"],
                    ]
                )
        if args.command == "patch":
            patches = patch.get(args)
            if args.detail:
                for p in patches["hits"]:
                    print(patch.format_detail(p))

                if patches["meta"]["total_hits"] > PATCH_WARN_NUMBER:
                    print_warn(
                        f"Your query has {patches['meta']['total_hits']} hits, you might want to refine your search criteria"
                    )
                print(
                    f"Page {patches['meta']['current_page']}/{patches['meta']['total_pages']}\t Hits: {patches['meta']['total_hits']}"
                )
                sys.exit(0)
            else:
                table.hrules = ALL
                table.field_names = [
                    "Severity",
                    "Name",
                    "Product",
                    "Arch",
                    "id",
                    "Released",
                ]
                for p in patches["hits"]:
                    table.add_row(
                        [
                            p["severity"],
                            p["title"],
                            "\n".join(p["product_friendly_names"]),
                            "\n".join(p["product_architectures"]),
                            p["ibs_id"],
                            p["issued_at"][: p["issued_at"].find("T")],
                        ]
                    )
                if patches["meta"]["total_hits"] > PATCH_WARN_NUMBER:
                    print("\n")
                    print_warn(
                        f"Your query has {patches['meta']['total_hits']} hits, you might want to refine your search criteria"
                    )
                print(
                    f"\nPage {patches['meta']['current_page']}/{patches['meta']['total_pages']}\t Hits: {patches['meta']['total_hits']}"
                )

        for name in table.field_names:
            table.align[name] = "l"
        table.border = not args.no_borders
        table.header = not args.no_header
        table.sortby = args.sort_table
        print(table)

    if args.command == "completion":
        print(completion.get(args.cache_file, args.shell))

    cacheages = cache.age(args.cache_file, args.cache_age)
    for key, value in cacheages.items():
        print_warn(f"The {key} cache is old, last updated {value}")
