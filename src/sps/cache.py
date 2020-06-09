import json
import sys
from pathlib import Path


def save(key, filename, data):
    """Saves cache to filename

    The cache is a json file and is loaded as dictionary.

    Parameters
    ---------
    key: str
        the dictionary key that the data should be accociated with.
    filename: str
        the path to filename to save the cache to
    data: list
        data to be saved in cache

    Returns
    -------
    None

    Raises
    ------
    SystemExit
        if key is not known
        if data is not of type list
        if PermissionError is raised when saving to filename
    """

    cache_data = {}
    if not key in ["product"]:
        print(f"Error: trying to save cache with unknown key '{key}'", file=sys.stderr)
        sys.exit(1)
    if not isinstance(data, list):
        print(f"Error: Must have list as data source to save cache", file=sys.stderr)
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
    """Load cache from filename

    The cache file is a json file and retruns a dictionary

    Parameters
    ----------
    filename: str
        path to the json file

    Returns
    -------
    dict
        the content of the cache json file as dict

    Raises
    ------
    SystemExit
        If PermissionError raises
        if unable to decode cache file as JSON
    """

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
    """Lookup a product in the cache

    Lookup a product in cache based on identifier and return the id

    Parameters
    ----------
    identifier: str
        product identifier to search for
    filename: str
        path to cache file to use

    Returns
    -------
    int
        the product id

    Raises
    ------
    SystemExit
        if no product matches the identifier
    """

    data = load(filename)
    for product in data["product"]:
        if product["identifier"] == identifier:
            return product["id"]
    print(f"Couldn't find id for '{identifier}'", file=sys.stderr)
    sys.exit(1)
