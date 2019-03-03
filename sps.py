#!/usr/bin/env python
import json
import certifi
import pycurl
import click
import sys
import os
import pickle
from prettytable import PrettyTable
from io import BytesIO
from pathlib import Path

URL_PRODUCTS = "https://scc.suse.com/api/package_search/products"
URL_PACKAGES = "https://scc.suse.com/api/package_search/packages"

PRODUCT_CACHE_PATH = '{}/.cache/sps'.format(Path.home())


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
        sys.stderr.write('Error: {}\n'.format(e.args[1]))
        sys.exit(e.args[0])



def get_products(search, field, update_cache):
    cache_file = "{}/products".format(PRODUCT_CACHE_PATH)

    if update_cache or not os.path.isfile(cache_file):
        response = fetch(URL_PRODUCTS)
    else:
        response = pickle.load(open(cache_file, 'rb' ))
    if update_cache:
        cache_path = Path(PRODUCT_CACHE_PATH)
        if not cache_path.exists():
            try:
                os.mkdir(PRODUCT_CACHE_PATH)
            except (FileExistsError, PermissionError) as e:
                sys.exit('Error: {}'.format(e))
        try:
            pickle.dump(response, open(cache_file, 'wb'))
        except PermissionError as e:
            sys.exit('Error: {}'.format(e))


    products = []
    if search == "*":
        products = response
    else:
        for product in response:
            if search in product[field]:
                products.append(product)
    return products


def completion_bash():
    comp = """
_sps_complete()
{
	local cur_word prev_word type_list
	cur_word="${COMP_WORDS[COMP_CWORD]}"
	prev_word="${COMP_WORDS[COMP_CWORD-1]}"

	if [[ "$prev_word" == "sps" ]];then
		type_list="--help package product completion"
	elif [[ "$prev_word" == "package" ]];then
		type_list="--help --product"
	elif [[ "$prev_word" == "product" ]];then
		type_list="--help --field --update-cache"
	elif [[ "$prev_word" == "completion" ]];then
		type_list="--help bash"
	fi

	if [[ "${type_list}x" == "x" ]];then
		COMPREPLY=()
	else
		COMPREPLY=( $(compgen -W "${type_list}" -- ${cur_word}) )
	fi
	return 0
}
complete -F _sps_complete sps
"""
    print(comp)


@click.group()
@click.pass_context
def main(ctx):
    pass


@main.command()
@click.option("--product", required=True, default=0, help="id of product to search in")
@click.argument("pattern")
@click.pass_context
def package(ctx, product, pattern):
    """Search for packages"""
    url = "{}?product_id={}&query={}".format(URL_PACKAGES, product, pattern)
    packages = fetch(url)
    table = PrettyTable()
    table.field_names = ["Name", "Version", "Release", "Arch", "Module(s)"]
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
    print(table)


@main.command()
@click.argument("pattern", default="*")
@click.option(
    "--field",
    help="Search PATTERN in this field, default=identifier",
    default="identifier",
    type=click.Choice(["name", "identifier", "edition"]),
)
@click.option('--update-cache', is_flag=True, help='Update the local product cache')
@click.pass_context
def product(ctx, pattern, field, update_cache):
    """Search for products"""
    products = get_products(pattern, field, update_cache)
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
    print(table)


@main.command()
@click.argument("shell", type=click.Choice(["bash"]))
@click.pass_context
def completion(ctx, shell):
    """Completion for shells"""
    if shell == "bash":
        completion_bash()


if __name__ == "__main__":
    main(obj={})
