import sys
from sps import request, cache


def get(product, pattern, cache_filename):
    try:
        product_id = int(product)
    except ValueError:
        product_id = cache.lookup(product, cache_filename)

    url = f"https://scc.suse.com/api/package_search/packages?product_id={product_id}&query={pattern}"
    response = request.fetch(url)
    try:
        response["data"]
    except KeyError as err:
        print(f"Error: No data key found, {err}", file=sys.stderr)
        sys.exit(1)
    return response
