import pytest
import json
import os
from argparse import Namespace
from sps import cache, cli, patch
from sps.helpers import CWARNING, CRESET


@pytest.fixture
def data():
    filename = f"{os.path.dirname(os.path.realpath(__file__))}/patch_reply.json"
    with open(filename, "r") as f:
        d = json.load(f)
    return d


@pytest.fixture
def parser():
    class P:
        command = "patch"
        pattern = None
        cache_file = "fake-file-name"
        update_cache = False
        cache_age = 60
        no_cache = False
        no_borders = False
        no_header = False
        sort_table = "Released"
        only_security_patches = False
        date_from = None
        date_to = None
        page = 1
        product = None
        arch = None
        product_version = None
        detail = False

        def parse_args(self):
            return Namespace(
                command=self.command,
                pattern=self.pattern,
                cache_file=self.cache_file,
                update_cache=self.update_cache,
                cache_age=self.cache_age,
                no_cache=self.no_cache,
                no_borders=self.no_borders,
                no_header=self.no_header,
                sort_table=self.sort_table,
                only_security_patches=self.only_security_patches,
                date_from=self.date_from,
                date_to=self.date_to,
                page=self.page,
                product=self.product,
                arch=self.arch,
                product_version=self.product_version,
                detail=self.detail,
            )

    return P


def test_cli_main_patch(mocker, capsys, data, parser):
    mocker.patch("sps.cache.age")
    cache.age.return_value = {}
    mocker.patch("sps.patch.get")
    patch.get.return_value = data
    mocker.patch("sps.cli.create_parser")
    p = parser()
    cli.create_parser.return_value = p
    output = "\nPage 1/9\t Hits: 81\n+-----------+--------------------------------------+----------------------------------------------------------+---------+------------------------------+------------+\n| Severity  | Name                                 | Product                                                  | Arch    | id                           | Released   |\n+-----------+--------------------------------------+----------------------------------------------------------+---------+------------------------------+------------+\n| important | Security update for the Linux Kernel | SUSE Linux Enterprise High Availability Extension 12 SP3 | ppc64le | SUSE-SLE-HA-12-SP3-2020-1275 | 2020-05-14 |\n|           |                                      | SUSE Linux Enterprise Server for SAP Applications 12 SP3 |         |                              |            |\n+-----------+--------------------------------------+----------------------------------------------------------+---------+------------------------------+------------+\n"

    cli.main()
    captured = capsys.readouterr()
    assert captured.out == output


def test_cli_main_patch_detail(mocker, capsys, data, parser):
    mocker.patch("sps.cache.age")
    cache.age.return_value = {}
    mocker.patch("sps.patch.get")
    patch.get.return_value = data
    mocker.patch("sps.cli.create_parser")
    p = parser()
    p.detail = True
    cli.create_parser.return_value = p
    output = """Detailed patch information
---------------------------------------------------------------------------
Name:		Security update for the Linux Kernel
Id:		SUSE-SLE-HA-12-SP3-2020-1275
Severity:	important
Released:	2020-05-14
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
          ocfs2-kmp-default-4.4.180-94.116.1.ppc64le.rpm
Page 1/9	 Hits: 81
"""
    with pytest.raises(SystemExit):
        cli.main()
    captured = capsys.readouterr()
    assert captured.out == output


def test_cli_main_patch_to_many_hits_warning(mocker, data, parser):
    mocker.patch("sps.cache.age")
    cache.age.return_value = {}
    mocker.patch("sps.patch.get")
    data["meta"]["total_hits"] = 501
    patch.get.return_value = data
    mocker.patch("sps.cli.create_parser")
    p = parser()
    cli.create_parser.return_value = p
    mocker.patch("sps.cli.print_warn")
    cli.main()
    cli.print_warn.assert_called_with(
        "Your query has 501 hits, you might want to refine your search criteria"
    )


def test_cli_main_patch_detail_to_many_hits_warning(mocker, data, parser):
    mocker.patch("sps.cache.age")
    cache.age.return_value = {}
    mocker.patch("sps.patch.get")
    data["meta"]["total_hits"] = 501
    patch.get.return_value = data
    mocker.patch("sps.cli.create_parser")
    p = parser()
    p.detail = True
    cli.create_parser.return_value = p
    mocker.patch("sps.cli.print_warn")
    with pytest.raises(SystemExit):
        cli.main()
    cli.print_warn.assert_called_with(
        "Your query has 501 hits, you might want to refine your search criteria"
    )


def test_cli_main_patch_no_hits_warning(mocker, capsys, data, parser):
    mocker.patch("sps.cache.age")
    cache.age.return_value = {}
    mocker.patch("sps.patch.get")
    data["meta"]["total_hits"] = 499
    patch.get.return_value = data
    mocker.patch("sps.cli.create_parser")
    p = parser()
    cli.create_parser.return_value = p
    output = ""
    cli.main()
    captured = capsys.readouterr()
    assert captured.err.strip() == output


def test_cli_main_patch_detail_no_hits_warning(mocker, capsys, data, parser):
    mocker.patch("sps.cache.age")
    cache.age.return_value = {}
    mocker.patch("sps.patch.get")
    data["meta"]["total_hits"] = 499
    patch.get.return_value = data
    mocker.patch("sps.cli.create_parser")
    p = parser()
    p.detail = True
    cli.create_parser.return_value = p
    output = ""
    with pytest.raises(SystemExit):
        cli.main()
    captured = capsys.readouterr()
    assert captured.err.strip() == output
