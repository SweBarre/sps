import pytest
import requests
import json
from sps import request


@pytest.fixture
def response():
    class Response:
        status_code = 200

        def json():
            return {"foo": "bar"}

    return Response


def test_request_fetch(response, mocker):
    """
    fetch content from URL
    """
    mocker.patch("requests.get", autospec=True)
    requests.get.return_value = response
    request.fetch("http://localhost")
    requests.get.assert_called_with("http://localhost", request.headers)


def test_request_fetch_bogus_url():
    """
    fetch will exit with bogus URL
    """
    with pytest.raises(SystemExit):
        request.fetch("lsdfjlsdjf")


def test_request_fetch_no_200_return_code(response, mocker):
    """
    fetch will exit if return code is not 200
    """
    mocker.patch("requests.get", autospec=True)
    response.status_code = 500
    requests.get.return_value = response
    with pytest.raises(SystemExit):
        request.fetch("http://localhost")


def test_request_fetch_with_json_response(response, mocker):
    """
    fetch will not exit with valid json response
    """
    mocker.patch("requests.get", autospec=True)
    requests.get.return_value = response
    assert request.fetch("http://localhost") == {"foo": "bar"}


def test_request_fetch_with_json_response(mocker):
    """
    fetch will exit with unvalid json response
    """

    class Response:
        status_code = 200

        def json(self):
            raise json.decoder.JSONDecodeError("foo", "bar", 0)

    response = Response()
    mocker.patch("requests.get", autospec=True)
    requests.get.return_value = response
    with pytest.raises(SystemExit):
        request.fetch("http://localhost")
