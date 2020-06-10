import re
import json
import sys
from pathlib import Path
from typing import List
from sps import request, cache
from sps.helpers import print_err


def get(pattern, cachefile, no_cache, update_cache) -> List:
    """Fetch the products used by SCC Patches

    Parameters
    ----------
    pattern: str
        Only return products where 'pattern' matches product name
    cachefile: str
        Patch to cache file
    no_cache: bool
        If true the cache file will not be used
    update_cache: bool
        if true the cache file will be updated

    Returns:
    List
        A list of Dict representing the products

    Raises:
    SystemExit
        if response from SUSE Customer Center is not parsable
    """

    data = {}
    if not update_cache and (
        Path(cachefile).exists() and Path(cachefile).is_file() and not no_cache
    ):
        data = cache.load(cachefile)
        try:
            data["patchproducts"]
        except KeyError as err:
            print_err("no patch product key found in cachefile")
            sys.exit(1)
    else:
        response = request.fetch("https://scc.suse.com/patches", "html")
        matches = re.findall(".*productsData=(.*)[^ \t\n\r\f\v]+.*", response)
        if len(matches) != 1:
            if len(matches) > 1:
                print_err("to many matches in response from SCC")
            else:
                print_err("no matches in response from SCC")
            exit(1)
        try:
            data["patchproducts"] = json.loads(matches[0])
        except json.decoder.JSONDecodeError as err:
            print_err(f"Couldn't parse json response {err}")
            sys.exit(1)

    ret = []
    if not pattern:
        ret = data["patchproducts"]
    else:
        for product in data["patchproducts"]:
            for k in product.keys():
                if pattern in str(product[k]):
                    ret.append(product)
                    break

    if update_cache:
        cache.save("patchproducts", cachefile, data["patchproducts"])
    return ret


def short(products, field):
    """Creates a bash completion list for data

    Parameters
    ----------
    products: list
        list of products data
    field: str
        the field name that should be formated

    Returns
    -------
    str
        formated string with unique fields and spces converted to underscore
    """

    li = []
    for p in products:
        if not p[field].replace(" ", "_") in li:
            li.append(p[field].replace(" ", "_"))
    return li
