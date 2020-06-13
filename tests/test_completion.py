import os
import pytest
from sps import completion, cache


@pytest.fixture
def data():
    return {
        "patchproducts": [
            {"name": "Legacy Module", "version": "15 SP2", "architecture": "aarch64",},
            {
                "name": "SUSE Linux Enterprise Server for SAP Applications",
                "version": "15 SP2",
                "architecture": "x86_64",
            },
        ],
        "product": [
            {
                "id": 1713,
                "name": "SUSE CaaS Platform",
                "identifier": "CAASP/3.0/x86_64",
                "type": "base",
                "free": False,
                "edition": "3.0",
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
        ],
    }


@pytest.fixture
def expected_result():
    with open("src/sps/completion.sh", "r") as f:
        fc = f.read()
    fc = fc.replace(
        "{sps_patch_product_complete}",
        "Legacy_Module SUSE_Linux_Enterprise_Server_for_SAP_Applications",
    )
    fc = fc.replace("{sps_patch_version_complete}", "15_SP2")
    fc = fc.replace("{sps_patch_arch_complete}", "aarch64 x86_64")
    fc = fc.replace(
        "{sps_package_product_complete}", "CAASP/3.0/x86_64 SLED/15.2/x86_64"
    )
    return fc


def test_completion_bash(mocker, data, expected_result):
    mocker.patch("sps.cache.load")
    cache.load.return_value = data
    assert completion.get("/path/to/cache/file", "bash") == expected_result


def test_completion_environment(mocker, data, expected_result):
    mocker.patch("sps.cache.load")
    cache.load.return_value = data

    os.environ["SHELL"] = "/bin/bash"
    assert completion.get("/path/to/cache/file", "bash") == expected_result
    os.environ.pop(("SHELL"))
    with pytest.raises(SystemExit):
        completion.get("/path/tho/cache/file")


def test_completion_unknown_shell():
    os.environ["SHELL"] = "/path/to/unknown/shell/bad-shell-name"
    with pytest.raises(SystemExit):
        completion.get("/path/tho/cache/file")


def test_completion_sourcefile_not_found(mocker):
    mocker.patch("builtins.open", side_effect=FileNotFoundError("no such file"))
    with pytest.raises(SystemExit):
        completion.get("/path/to/cache/file", "bash")
