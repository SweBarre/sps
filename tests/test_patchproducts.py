import pytest
import json
from sps import cache, request, patchproducts


@pytest.fixture
def data():
    return [
        {"name": "Legacy Module", "version": "15 SP2", "architecture": "aarch64"},
        {
            "name": "SUSE Linux Enterprise Server for SAP Applications",
            "version": "15 SP2",
            "architecture": "x86_64",
        },
        {
            "name": "SUSE Linux Enterprise Real Time Extension",
            "version": "12 SP1",
            "architecture": "x86_64",
        },
        {"name": "Development Tools Module", "version": "15", "architecture": "s390x"},
    ]


@pytest.fixture
def patchproducts_data():
    return [
        {"name": "Legacy Module", "version": "15 SP2", "architecture": "aarch64",},
        {
            "name": "SUSE Linux Enterprise Server for SAP Applications",
            "version": "15 SP2",
            "architecture": "x86_64",
        },
        {
            "name": "SUSE Linux Enterprise Real Time Extension",
            "version": "12 SP1",
            "architecture": "x86_64",
        },
        {"name": "Development Tools Module", "version": "15", "architecture": "s390x",},
    ]


def test_patchproducts_get(mocker, data, patchproducts_data):
    mocker.patch("sps.request.fetch", autospec=True)
    request.fetch.return_value = (
        f"aöskdföskdföproductsData={json.dumps(data)};\nslkdfjsal"
    )
    assert patchproducts.get(None, "fake-file-name", False, False) == patchproducts_data
    request.fetch.assert_called_with("https://scc.suse.com/patches", "html")


def test_patchproducts_get_pattern_multipple_match(mocker, data, patchproducts_data):
    mocker.patch("sps.request.fetch", autospec=True)
    request.fetch.return_value = data
    request.fetch.return_value = (
        f"aöskdföskdföproductsData={json.dumps(data)};\nslkdfjsal"
    )
    expected_return = []
    for product in patchproducts_data:
        for k in product.keys():
            if "SUSE" in str(product[k]):
                expected_return.append(product)
                break
    assert patchproducts.get("SUSE", "fake-file-name", False, False) == expected_return


def test_patchproducts_get_pattern_single_match(mocker, data, patchproducts_data):
    mocker.patch("sps.request.fetch")
    request.fetch.return_value = (
        f"aöskdföskdföproductsData={json.dumps(data)};\nslkdfjsal"
    )
    expected_return = []
    for product in patchproducts_data:
        for k in product.keys():
            if "Legacy Module" in str(product[k]):
                expected_return.append(product)
                break
    assert (
        patchproducts.get("Legacy Module", "fake-file-name", False, False)
        == expected_return
    )


def test_patchproducts_get_pattern_no_match(mocker, data):
    mocker.patch("sps.request.fetch", autospec=True)
    request.fetch.return_value = (
        f"aöskdföskdföproductsData={json.dumps(data)};\nslkdfjsal"
    )
    assert patchproducts.get("no-hit-", "fake-file-name", False, False) == []


def test_patchproducts_get_cache(mocker, patchproducts_data):
    mocker.patch("sps.cache.load", autospec=True)
    cache.load.return_value = {"patchproducts": patchproducts_data}
    assert patchproducts.get(None, __file__, False, False) == patchproducts_data


def test_patchproducts_update_cache(mocker, data, patchproducts_data):
    mocker.patch("sps.cache.save", autospec=True)
    mocker.patch("sps.request.fetch", autospec=True)
    request.fetch.return_value = (
        f"aöskdföskdföproductsData={json.dumps(data)};\nslkdfjsal"
    )
    patchproducts.get(None, "fake-file-name", False, True)
    cache.save.assert_called_with("patchproducts", "fake-file-name", patchproducts_data)


def test_patchproducts_cache_no_key(mocker):
    mocker.patch("sps.cache.load", autospec=True)
    cache.load.return_value = {"data": [1, 2, 3]}
    with pytest.raises(SystemExit):
        patchproducts.get(None, __file__, False, False)


def test_patchproducts_to_many_matches_from_scc(mocker, data):
    mocker.patch("sps.cache.save", autospec=True)
    mocker.patch("sps.request.fetch", autospec=True)
    request.fetch.return_value = f"aöskdföskdföproductsData={json.dumps(data)};\nslkdfjsalaöskdföskdföproductsData={json.dumps(data)};\nslkdfjsal"
    with pytest.raises(SystemExit):
        patchproducts.get(None, "fake-file-name", False, False)


def test_patchproducts_no_matches_from_scc(mocker, data):
    mocker.patch("sps.cache.save", autospec=True)
    mocker.patch("sps.request.fetch", autospec=True)
    request.fetch.return_value = f"aöskdföskdföprodsData={json.dumps(data)};\nslkdfjsalaöskdföskdföproduata={json.dumps(data)};\nslkdfjsal"
    with pytest.raises(SystemExit):
        patchproducts.get(None, "fake-file-name", False, False)


def test_patchproducts_json_parse_error(mocker, data):
    mocker.patch("sps.cache.save", autospec=True)
    mocker.patch("sps.request.fetch", autospec=True)
    request.fetch.return_value = f"aöskdföskdföproductsData={data};\nslkdfjsal"
    with pytest.raises(SystemExit):
        patchproducts.get(None, "fake-file-name", False, False)
