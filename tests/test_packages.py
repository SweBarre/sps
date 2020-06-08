import pytest
import requests
from sps import request, packages, cache


@pytest.fixture
def requests_response():
    class Response:
        status_code = 200

        def json():
            return {"data": [{"foo": "bar"}]}

    return Response


@pytest.fixture
def requests_bad_response():
    class Response:
        status_code = 200

        def json():
            return {"bad": [{"foo": "bar"}]}

    return Response


def test_product_get_with_id(mocker, requests_response):
    """
    get with product id will not exit
    """
    mocker.patch("requests.get", autospec=True)
    requests.get.return_value = requests_response
    assert packages.get(1899, "vim", "filename") == {"data": [{"foo": "bar"}]}
    requests.get.assert_called_with(
        "https://scc.suse.com/api/package_search/packages?product_id=1899&query=vim",
        request.headers,
    )


def test_product_get_with_product_identifier(mocker, requests_response):
    """
    get with product name will not exit
    """
    mocker.patch("requests.get", autospec=True)
    requests.get.return_value = requests_response
    mocker.patch("sps.cache.lookup_product", autospec=True)
    cache.lookup_product.return_value = 1899
    packages.get("SLED/15.2/x86_64", "vim", "filename")
    requests.get.assert_called_with(
        "https://scc.suse.com/api/package_search/packages?product_id=1899&query=vim",
        request.headers,
    )


def test_product_get_with_bad_respone(mocker, requests_bad_response):
    """
    get with product id will exit
    """
    mocker.patch("requests.get", autospec=True)
    requests.get.return_value = requests_bad_response
    with pytest.raises(SystemExit):
        packages.get(12, "vim", "filename")
