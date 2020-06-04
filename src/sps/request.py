import requests
import sys
import json


headers = {"Accept": "application/vnd.scc.suse.com.v4+json"}


def fetch(url):
    try:
        response = requests.get(url, headers)
    except requests.exceptions.RequestException as err:
        print(f"Error: {err}", file=sys.stderr)
        sys.exit(1)
    if response.status_code != 200:
        print(
            f"Error: Got status code '{response.status_code}' from {url}",
            file=sys.stderr,
        )
        sys.exit(1)
    try:
        return response.json()
    except json.decoder.JSONDecodeError as err:
        print(f"Error: Couldn't parse json response {err}")
        sys.exit(1)
