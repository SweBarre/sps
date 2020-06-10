import pytest
from argparse import ArgumentParser, Namespace
from prettytable import PrettyTable
import prettytable
from pathlib import Path
from sps import helpers, cli, products, packages, completion, cache, __version__


@pytest.fixture
def data():
    return {
        "product": [
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


def test_main_product_output(mocker, capsys):
    class parser_proxy:
        def parse_args(self):
            return Namespace(
                command="product",
                pattern=None,
                cache_file="fake-file-name",
                update_cache=False,
                no_cache=False,
                no_borders=False,
                no_header=False,
                sort_table="id",
                cache_age=60,
            )

    data = {
        "data": [
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

    mocker.patch("sps.cache.age", autospec=True)
    cache.age.return_value = {}
    mocker.patch("sps.products.get", autospec=True)
    products.get.return_value = data["data"]
    mocker.patch("sps.cli.create_parser", autospec=True)
    cli.create_parser.return_value = parser_proxy()

    output = """+------+-------------------------------+---------+------------------+--------+
| id   | Name                          | Edition | Identifier       | Arch   |
+------+-------------------------------+---------+------------------+--------+
| 1935 | SUSE Linux Enterprise Desktop | 15 SP2  | SLED/15.2/x86_64 | x86_64 |
+------+-------------------------------+---------+------------------+--------+
"""

    cli.main()
    captured = capsys.readouterr()
    assert captured.out == output


def test_main_package_output(mocker, capsys):
    class parser_proxy:
        def parse_args(self):
            return Namespace(
                command="package",
                pattern="gvim",
                cache_file="fake-file-name",
                update_cache=False,
                product="1935",
                exact_match=False,
                no_borders=False,
                no_header=False,
                sort_table="Name",
                cache_age=60,
            )

    data = {
        "data": [
            {
                "id": 19399264,
                "name": "gvim",
                "arch": "x86_64",
                "version": "8.0.1568",
                "release": "5.3.1",
                "products": [
                    {
                        "id": 1967,
                        "name": "Desktop Applications Module",
                        "identifier": "sle-module-desktop-applications/15.2/x86_64",
                        "type": "module",
                        "free": True,
                        "edition": "15 SP2",
                        "architecture": "x86_64",
                    }
                ],
            },
            {
                "id": 19731289,
                "name": "gvim-debuginfo",
                "arch": "x86_64",
                "version": "8.0.1568",
                "release": "5.3.1",
                "products": [
                    {
                        "id": 1967,
                        "name": "Desktop Applications Module",
                        "identifier": "sle-module-desktop-applications/15.2/x86_64",
                        "type": "module",
                        "free": True,
                        "edition": "15 SP2",
                        "architecture": "x86_64",
                    }
                ],
            },
        ]
    }

    mocker.patch("sps.cache.age", autospec=True)
    cache.age.return_value = {}
    mocker.patch("sps.packages.get", autospec=True)
    packages.get.return_value = data["data"]
    mocker.patch("sps.cli.create_parser", autospec=True)
    cli.create_parser.return_value = parser_proxy()

    output = """+----------------+----------+---------+--------+-----------------------------+
| Name           | Version  | Release | Arch   | Module                      |
+----------------+----------+---------+--------+-----------------------------+
| gvim           | 8.0.1568 | 5.3.1   | x86_64 | Desktop Applications Module |
| gvim-debuginfo | 8.0.1568 | 5.3.1   | x86_64 | Desktop Applications Module |
+----------------+----------+---------+--------+-----------------------------+
"""

    cli.main()
    captured = capsys.readouterr()
    assert captured.out == output


def test_main_package_output_exact_match(mocker, capsys):
    class parser_proxy:
        def parse_args(self):
            return Namespace(
                command="package",
                pattern="gvim",
                cache_file="fake-file-name",
                update_cache=False,
                product="1935",
                exact_match=True,
                no_borders=False,
                no_header=False,
                sort_table="Name",
                cache_age=60,
            )

    data = {
        "data": [
            {
                "id": 19399264,
                "name": "gvim",
                "arch": "x86_64",
                "version": "8.0.1568",
                "release": "5.3.1",
                "products": [
                    {
                        "id": 1967,
                        "name": "Desktop Applications Module",
                        "identifier": "sle-module-desktop-applications/15.2/x86_64",
                        "type": "module",
                        "free": True,
                        "edition": "15 SP2",
                        "architecture": "x86_64",
                    }
                ],
            },
            {
                "id": 19731289,
                "name": "gvim-debuginfo",
                "arch": "x86_64",
                "version": "8.0.1568",
                "release": "5.3.1",
                "products": [
                    {
                        "id": 1967,
                        "name": "Desktop Applications Module",
                        "identifier": "sle-module-desktop-applications/15.2/x86_64",
                        "type": "module",
                        "free": True,
                        "edition": "15 SP2",
                        "architecture": "x86_64",
                    }
                ],
            },
        ]
    }

    mocker.patch("sps.cache.age", autospec=True)
    cache.age.return_value = {}
    mocker.patch("sps.packages.get", autospec=True)
    packages.get.return_value = data["data"]
    mocker.patch("sps.cli.create_parser", autospec=True)
    cli.create_parser.return_value = parser_proxy()

    output = """+------+----------+---------+--------+-----------------------------+
| Name | Version  | Release | Arch   | Module                      |
+------+----------+---------+--------+-----------------------------+
| gvim | 8.0.1568 | 5.3.1   | x86_64 | Desktop Applications Module |
+------+----------+---------+--------+-----------------------------+
"""

    cli.main()
    captured = capsys.readouterr()
    assert captured.out == output


def test_main_completion(mocker):
    class parser_proxy:
        def parse_args(self):
            return Namespace(
                command="completion",
                cache_file="fake-file-name",
                shell="bash",
                cache_age=60,
            )

    mocker.patch("sps.cache.age", autospec=True)
    cache.age.return_values = {}
    mocker.patch("sps.cli.create_parser", autospec=True)
    cli.create_parser.return_value = parser_proxy()
    mocker.patch("sps.completion.get", autospec=True)
    completion.get.return_value = "\n"
    cli.main()
    completion.get.assert_called_with("fake-file-name", "bash")


def test_main_aged_cache_no_return(mocker, capsys, data):
    class parser_proxy:
        def parse_args(self):
            return Namespace(
                command="product",
                pattern=None,
                cache_file="fake-file-name",
                update_cache=False,
                no_cache=False,
                no_borders=False,
                no_header=False,
                sort_table="id",
                cache_age=60,
            )

    mocker.patch("sps.cli.PrettyTable", autospec=True)
    mocker.patch("sps.cli.create_parser", autospec=True)
    cli.create_parser.return_value = parser_proxy()
    mocker.patch("sps.products.get", autospec=True)
    products.get.return_value = {}
    mocker.patch("sps.cache.age", autospec=True)
    cache.age.return_value = {}
    cli.main()
    cache.age.assert_called_once_with("fake-file-name", 60)
    cache.age.return_value = {"testing": "date"}
    cli.main()
    captured = capsys.readouterr()
    assert (
        captured.err.strip()
        == f"{helpers.CWARNING}Warning:{helpers.CRESET} The testing cache is old, last updated date"
    )
