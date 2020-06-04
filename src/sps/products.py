import sys
from pathlib import Path
from sps import request, cache


def get(pattern, cache_filename, no_cache, update_cache):
    cache_path = Path(cache_filename)
    if cache_path.exists() and cache_path.is_file() and not no_cache:
        response = cache.load(cache_filename)
    else:
        response = request.fetch("https://scc.suse.com/api/package_search/products")
    try:
        response["data"]
    except KeyError as err:
        print(f"Error: No data key found, {err}", file=sys.stderr)
        sys.exit(1)

    if update_cache:
        cache.save(cache_filename, response)
    ret = {"data": []}
    if not pattern:
        ret = response
    else:
        for product in response["data"]:
            for k in product.keys():
                if pattern in str(product[k]):
                    ret["data"].append(product)
                    break

    return ret
