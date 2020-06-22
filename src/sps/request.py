import requests
import sys
import json
from sps import __version__
from sps.helpers import print_err


headers = {
    "Accept": "application/vnd.scc.suse.com.v4+json",
    "User-Agent": f"sps/{__version__} https://github.com/SweBarre/sps",
}


def fetch(url, type="json"):
    try:
        response = requests.get(url, headers)
    except requests.exceptions.RequestException as err:
        print_err({err})
        sys.exit(1)
    if response.status_code != 200:
        print_err(f"Got status code '{response.status_code}' from {url}",)
        sys.exit(1)
    if type == "json":
        try:
            return response.json()
        except json.decoder.JSONDecodeError as err:
            print_err(f"Couldn't parse json response {err}")
            sys.exit(1)
    elif type == "html":
        return response.text
