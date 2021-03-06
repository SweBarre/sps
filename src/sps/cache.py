import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict
from sps.helpers import print_err


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
    if not key in ["product", "patchproducts"]:
        print_err(f"trying to save cache with unknown key '{key}'")
        sys.exit(1)
    if not isinstance(data, list):
        print_err("Must have list as data source to save cache")
        sys.exit(1)

    if Path(filename).is_file():
        cache_data = load(filename)

    cache_data[key] = data
    try:
        cache_data["age"][key] = datetime.now().strftime("%Y-%m-%d")
    except KeyError:
        cache_data["age"] = {}
        cache_data["age"][key] = datetime.now().strftime("%Y-%m-%d")

    try:
        with open(filename, "w") as f:
            json.dump(cache_data, f)
    except PermissionError as err:
        print_err({err})
        sys.exit(13)


def load(filename) -> Dict:
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

    data = {}
    try:
        with open(filename, "r") as f:
            data = json.load(f)
    except PermissionError as err:
        print_err({err})
        sys.exit(13)
    except json.decoder.JSONDecodeError as err:
        print_err(f"unable to parse {filename} as JSON, {err}")
        sys.exit(1)
    except FileNotFoundError:
        pass
    return data


def age(filename, age) -> Dict:
    """Check the age of the different elements in the cache

    Parameters
    ----------
    filename: str
        path to cache file
    age: int
        number of days that would indicate old cache data

    Returns
    -------
    list
        returns a list of cache elements that is old
        the key is the cache element as str
        the value is the date str %Y-%m-%d when the cache was saved
    """

    ret = {}
    cache_data = load(filename)
    now = datetime.now()
    if cache_data:
        for key, value in cache_data["age"].items():
            cacheage = now - datetime.strptime(value, "%Y-%m-%d")
            if cacheage.days > age:
                ret[key] = value
    return ret


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
    print_err(f"Couldn't find id for '{identifier}'")
    sys.exit(1)
