import sys
from sps import request, cache
from sps.helpers import print_err


def get(product, pattern, cache_filename):
    """Get the packages information from SUSE Customer Center
    for a particular product

    Parameters
    ----------
    product: str
        product id or identifier
    pattern: str
        search pattern in package name, if blank all packages will be
        returned
    cache_filename: str
        path to the cache file name to be used to lookup product id
        if product identifier is specified instead of product it

    Returns
    -------
    list
        a list of packages that matches the search result
        each package is a dict

    Raises
    ------
    SystemExit
        if the response from SUSE Customer Center is not parsable
    """

    try:
        product_id = int(product)
    except ValueError:
        product_id = cache.lookup_product(product, cache_filename)

    url = f"https://scc.suse.com/api/package_search/packages?product_id={product_id}&query={pattern}"
    response = request.fetch(url)
    try:
        response["data"]
    except KeyError as err:
        print_err(f"Error: No data key found, {err}")
        sys.exit(1)
    return response["data"]
