#!/usr/bin/env python
import json
import certifi
import pycurl
import click
import sys
import os
import pickle
import datetime
import atexit
from prettytable import PrettyTable
from colorama import Fore, Back, Style
from io import BytesIO
from pathlib import Path

URL_PRODUCTS = "https://scc.suse.com/api/package_search/products"
URL_PACKAGES = "https://scc.suse.com/api/package_search/packages"

PRODUCT_CACHE_PATH = "{}/.cache/sps".format(Path.home())
# how many days should pass before warning on old cache file
CACHE_WARNING_DAYS = 90


def exit_checks():
    """Thing that should be runing before exiting"""
    fname = "{}/products".format(PRODUCT_CACHE_PATH)
    if os.path.isfile(fname):
        today = datetime.datetime.today()
        filedate = datetime.datetime.fromtimestamp(os.path.getmtime(fname))
        fileage = today - filedate
        if fileage.days > CACHE_WARNING_DAYS:
            print(
                "{style}{color}WARNING: The products cahce for suse package search is {age} days old{reset}".format(
                    style=Style.BRIGHT,
                    color=Fore.YELLOW,
                    age=fileage.days,
                    reset=Style.RESET_ALL,
                )
            )


def fetch(url):
    buf = BytesIO()
    curl = pycurl.Curl()
    curl.setopt(curl.URL, url)
    curl.setopt(
        curl.HTTPHEADER,
        ["accept: application/json", "Accept: application/vnd.scc.suse.com.v4+json"],
    )
    curl.setopt(curl.WRITEDATA, buf)
    curl.setopt(curl.CAINFO, certifi.where())
    try:
        curl.perform()
        curl.close()
        response = json.loads(buf.getvalue().decode("utf-8"))
        return response["data"]
    except pycurl.error as e:
        sys.stderr.write("Error: {}\n".format(e.args[1]))
        sys.exit(e.args[0])


def get_products(search, field, update_cache, no_cache):
    cache_file = "{}/products".format(PRODUCT_CACHE_PATH)

    if update_cache or no_cache or not os.path.isfile(cache_file):
        response = fetch(URL_PRODUCTS)
    else:
        response = pickle.load(open(cache_file, "rb"))
    if update_cache:
        cache_path = Path(PRODUCT_CACHE_PATH)
        if not cache_path.exists():
            try:
                os.mkdir(PRODUCT_CACHE_PATH)
            except (FileExistsError, PermissionError) as e:
                sys.exit("Error: {}".format(e))
        try:
            pickle.dump(response, open(cache_file, "wb"))
        except PermissionError as e:
            sys.exit("Error: {}".format(e))

    products = []
    if search == "*":
        products = response
    else:
        for product in response:
            if search in product[field]:
                products.append(product)
    return products


@click.group()
@click.pass_context
def main(ctx):
    atexit.register(exit_checks)


@main.command()
@click.option("--product", required=True, help="id of product to search in")
@click.option(
    "--sort",
    type=click.Choice(["Name", "Version", "Release", "Arch", "Module"]),
    default=None,
    help="Select the sorting field",
)
@click.argument("pattern")
@click.pass_context
def package(ctx, product, sort, pattern):
    """Search for packages"""
    # check if product is int, if not search for the int in cache file
    try:
        product = int(product)
    except ValueError:
        products = get_products(product, "identifier", False, False)
        if len(products) > 1:
            print("Narrow down your product search, current selection gives:")
            for prod in products:
                print(" - {}".format(prod["identifier"]))
            sys.exit(1)
        if len(products) == 0:
            sys.stderr.write(
                'Error: Could not match "{}" to a product\n'.format(product)
            )
            sys.exit(1)
        product = products[0]["id"]
    url = "{}?product_id={}&query={}".format(URL_PACKAGES, product, pattern)
    packages = fetch(url)
    table = PrettyTable()
    table.field_names = ["Name", "Version", "Release", "Arch", "Module"]
    for name in table.field_names:
        table.align[name] = "l"
    for package in packages:
        module_line = ""
        for product in package["products"]:
            module_line = "{},{}".format(module_line, product["name"])
        table.add_row(
            [
                package["name"],
                package["version"],
                package["release"],
                package["arch"],
                module_line[1:],
            ]
        )
    if sort is not None:
        table.sortby = sort

    print(table)


@main.command()
@click.argument("pattern", default="*")
@click.option(
    "--field",
    help="Search PATTERN in this field, default=identifier",
    default="identifier",
    type=click.Choice(["name", "identifier", "edition"]),
)
@click.option("--update-cache", is_flag=True, help="Update the local product cache")
@click.option(
    "--no-cache",
    is_flag=True,
    help="Don not use local product cache, fetch from internet",
)
@click.option("--no-borders", is_flag=True, help="don't output borders")
@click.option("--no-header", is_flag=True, help="don't output header")
@click.option(
    "--short", is_flag=True, help="no borders or header, only field id and identifier"
)
@click.option(
    "--sort",
    type=click.Choice(["id", "Name", "Edition", "Identifier", "Arch"]),
    default=None,
    help="Select the sorting field",
)
@click.pass_context
def product(
    ctx, pattern, field, update_cache, no_cache, no_borders, no_header, short, sort
):
    """Search for products"""
    products = get_products(pattern, field, update_cache, no_cache)
    table = PrettyTable()
    table.field_names = ["id", "Name", "Edition", "Identifier", "Arch"]
    for name in table.field_names:
        table.align[name] = "l"
    for product in products:
        table.add_row(
            [
                product["id"],
                product["name"],
                product["edition"],
                product["identifier"],
                product["architecture"],
            ]
        )
    if sort is not None:
        table.sortby = sort
    table.border = not no_borders
    table.header = not no_header
    if short:
        table.border = False
        table.header = False
        print(table.get_string(fields=["Identifier"]))
    else:
        print(table)


@main.command()
@click.argument("shell", type=click.Choice(["bash"]))
@click.pass_context
def completion(ctx, shell):
    """Print out the shell completion functions"""
    if shell == "bash":
        fname = "{}/completion.sh".format(os.path.dirname(os.path.realpath(__file__)))
    f = open(fname, "r")
    print(f.read())
    f.close()


if __name__ == "__main__":
    main(obj={})
