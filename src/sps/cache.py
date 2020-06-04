import json
import sys


def save(filename, data):
    if not isinstance(data, dict):
        print(
            f"Error: Must have dictionary as data source to save cache", file=sys.stderr
        )
        sys.exit(1)
    try:
        with open(filename, "w") as f:
            json.dump(data, f)
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


def lookup(identifier, filename):
    data = load(filename)
    for product in data["data"]:
        if product["identifier"] == identifier:
            return product["id"]
    print(f"Couldn't find id for '{identifier}'", file=sys.stderr)
    sys.exit(1)
