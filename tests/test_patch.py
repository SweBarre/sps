import pytest
import json
import os
from argparse import Namespace
from sps import patch, request

url = "https://scc.suse.com/api/frontend/patch_finder/search/perform.json"


@pytest.fixture
def args():
    return Namespace(
        product="Legacy_Module",
        product_version="12",
        arch="x86_64",
        pattern="",
        severity="any",
        only_security_patches=False,
        date_from="",
        date_to="",
        page=1,
    )


@pytest.fixture
def data():
    fn = f"{os.path.dirname(os.path.realpath(__file__))}/patch_reply.json"
    with open(fn) as f:
        d = json.load(f)
    return d


def format_url(args):

    product = args.product if args.product else ""
    version = args.product_version if args.product_version else ""
    arch = args.arch if args.arch else ""
    product = product.replace("_", "+")
    version = version.replace("_", "+")

    if args.pattern:
        query = args.pattern.replace(" ", "+")
    else:
        query = ""
    security = "true" if args.only_security_patches else ""
    severity = "" if args.severity == "all" else args.severity

    url = "https://scc.suse.com/api/frontend/patch_finder/search/perform.json"
    url += f"?only_security_patches={security}"
    url += f"&page={args.page}"
    url += f"&product_architectures={arch}"
    url += f"&product_names={product}"
    url += f"&product_versions={version}"
    url += f"&q={query}"
    url += f"&severity={severity}"
    if args.date_to:
        url += f"&end_issued_at={args.date_to}"
    if args.date_from:
        url += f"&start_issued_at={args.date_from}"
    return url


def test_patch_get(mocker, args):
    mocker.patch("sps.request.fetch")
    patch.get(args)
    request.fetch.assert_called_with(format_url(args))


def test_patch_get_pattern(mocker, args):
    mocker.patch("sps.request.fetch")
    args.pattern = "Legacy Module"
    patch.get(args)
    request.fetch.assert_called_with(format_url(args))


def test_patch_get_severity(mocker, args):
    mocker.patch("sps.request.fetch")
    args.severity = "moderate"
    patch.get(args)
    request.fetch.assert_called_with(format_url(args))


def test_patch_get_all_products(mocker, args):
    mocker.patch("sps.request.fetch")
    args.product = None
    patch.get(args)
    request.fetch.assert_called_with(format_url(args))


def test_patch_get_date(mocker, args):
    mocker.patch("sps.request.fetch")
    args.date_from = "2020-06-01"
    args.date_to = "2020-12-31"
    patch.get(args)
    request.fetch.assert_called_with(format_url(args))


def test_patch_get_bad_date(mocker, args):
    mocker.patch("sps.request.fetch")
    args.date_to = "A B C"
    with pytest.raises(SystemExit):
        patch.get(args)

    args.date_to = ""
    args.date_from = "A B C"
    with pytest.raises(SystemExit):
        patch.get(args)


def test_patch_get_bad_response_from_scc(mocker, args):
    mocker.patch("sps.request.fetch")
    request.fetch.return_value = {}
    with pytest.raises(SystemExit):
        patch.get(args)


def test_patch_good_response_from_scc(mocker, args, data):
    mocker.patch("sps.request.fetch")
    request.fetch.return_value = data
    assert patch.get(args) == data


def test_patch_format_detail(data):
    expected_result = """Detailed patch information
---------------------------------------------------------------------------
Name:\t\tSecurity update for the Linux Kernel
Id:\t\tSUSE-SLE-HA-12-SP3-2020-1275
Severity:\timportant
Released:\t2020-05-14
Details:
description
References
    bugzilla: 
              1056134
    cve     : 
              CVE-2020-11609
Products: SUSE Linux Enterprise High Availability Extension 12 SP3 
SUSE Linux Enterprise Server for SAP Applications 12 SP3
Architecture: ppc64le
Packages: 
          ocfs2-kmp-default-4.4.180-94.116.1.ppc64le.rpm"""
    print(patch.format_detail(data["hits"][0]))
    assert patch.format_detail(data["hits"][0]) == expected_result
