import sys
from pathlib import Path
from sps import request, cache
from sps.helpers import print_err


def get(pattern, cache_filename, no_cache, update_cache):
    cache_path = Path(cache_filename)
    data = {}
    if cache_path.exists() and cache_path.is_file() and not no_cache:
        data = cache.load(cache_filename)
        try:
            data["product"]
        except KeyError as err:
            print_err("no product key found in cache file")
            sys.exit(1)
    else:
        response = request.fetch("https://scc.suse.com/api/package_search/products")
        try:
            data["product"] = response["data"]
        except KeyError as err:
            print_err(f"Error: No data key found in scc api response, {err}")
            sys.exit(1)

    ret = []
    if not pattern:
        ret = data["product"]
    else:
        for product in data["product"]:
            for k in product.keys():
                if pattern in str(product[k]):
                    ret.append(product)
                    break

    if update_cache:
        cache.save("product", cache_filename, ret)
    return ret
