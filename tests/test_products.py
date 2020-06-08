import pytest
from sps import products, request, cache


@pytest.fixture
def data():
    return {
        "data": [
            {
                "id": 1899,
                "name": "SUSE Manager Server",
                "identifier": "SUSE-Manager-Server/4.0/x86_64",
                "type": "base",
                "free": False,
                "edition": "4.0",
                "architecture": "x86_64",
            },
            {
                "id": 1935,
                "name": "SUSE Linux Enterprise Desktop",
                "identifier": "SLED/15.2/x86_64",
                "type": "base",
                "free": False,
                "edition": "15 SP2",
                "architecture": "x86_64",
            },
        ]
    }


def test_products_get(mocker, data):
    """
    get will return a list of all products
    """
    mocker.patch("sps.request.fetch", autospec=True)
    request.fetch.return_value = data
    assert products.get(None, "fake-file-name", False, False)
    request.fetch.assert_called_with("https://scc.suse.com/api/package_search/products")


def test_products_get_pattern_multiple_match(data, mocker):
    """
    get will return a list of all products matching pattern
    """
    mocker.patch("sps.request.fetch", autospec=True)
    request.fetch.return_value = data
    assert products.get("1", "fake-file-name", False, False) == data["data"]
    assert products.get("SUSE", "fake-file-name", False, False) == data["data"]
    assert products.get("x86", "fake-file-name", False, False) == data["data"]


def test_products_get_pattern_single_match(data, mocker):
    """
    get will return a list of all products matching pattern
    """
    mocker.patch("sps.request.fetch", autospec=True)
    request.fetch.return_value = data
    assert products.get("Manager", "fake-file-name", False, False) == [data["data"][0]]
    assert products.get("Desktop", "fake-file-name", False, False) == [data["data"][1]]


def test_products_get_pattern_no_match(data, mocker):
    """
    get will return a list of all products matching pattern
    """
    mocker.patch("sps.request.fetch", autospec=True)
    request.fetch.return_value = data
    assert products.get("foo-bar-search", "fake-file-name", False, False) == []


def test_products_get(data, mocker):
    """
    get will exit if no data field is found in response
    """
    mocker.patch("sps.request.fetch", autospec=True)
    wrongdata = {}
    wrongdata["bad"] = data["data"]
    request.fetch.return_value = wrongdata
    with pytest.raises(SystemExit):
        products.get(None, "fake-file-name", False, False)


def test_products_get_wrong_cache_data(data, mocker):
    """
    get will exit if no data field is found in response from cache
    """
    mocker.patch("sps.cache.load", autospec=True)
    cache.load.return_value = data
    with pytest.raises(SystemExit):
        products.get(None, __file__, False, False)


def test_products_get_cache(data, mocker):
    """
    get wtil retrieve products from cache file
    """
    mocker.patch("sps.cache.load", autospec=True)
    cache.load.return_value = {"product": data["data"]}
    assert products.get(None, __file__, False, False) == data["data"]


def test_products_update_cache(data, mocker):
    """
    get wtil retrieve products from cache file
    """
    mocker.patch("sps.cache.save", autospec=True)
    mocker.patch("sps.request.fetch", autospec=True)
    request.fetch.return_value = data
    products.get(None, "fake-file-name", False, True)
    cache.save.assert_called_with("product", "fake-file-name", data["data"])
