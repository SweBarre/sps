import json
import sys
from pathlib import Path


def save(key, filename, data):
    cache_data = {}
    if not key in ["product"]:
        print(
            f"Error: trying to save cache with unknown key '{key}'", file=sys.stderr
        )
        sys.exit(1)
    if not isinstance(data, list):
        print(
            f"Error: Must have list as data source to save cache", file=sys.stderr
        )
        sys.exit(1)

    if Path(filename).is_file():
        cache_data = load(filename)

    cache_data[key] = data

    try:
        with open(filename, "w") as f:
            json.dump(cache_data, f)
    except PermissionError as err:
        print(f"Error: {err}", file=sys.stderr)
        sys.exit(13)


def load(filename):
    try:
        with open(filename, "r") as f:
            data = json.load(f)
    except PermissionError as err:
        print(f"Error: {err}", file=sys.stderr)
        sys.exit(13)
    except json.decoder.JSONDecodeError as err:
        print(f"Error: unable to parse {filename} as JSON, {err}", file=sys.stderr)
        sys.exit(1)
    return data


def lookup_product(identifier, filename):
    data = load(filename)
    for product in data["product"]:
        if product["identifier"] == identifier:
            return product["id"]
    print(f"Couldn't find id for '{identifier}'", file=sys.stderr)
    sys.exit(1)
