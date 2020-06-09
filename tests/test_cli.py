import pytest
from argparse import ArgumentParser, Namespace
from prettytable import PrettyTable
import prettytable
from pathlib import Path
from sps import cli, products, packages, completion, cache, __version__


@pytest.fixture
def parser():
    return cli.create_parser([])


@pytest.fixture
def parser_product():
    return cli.create_parser(["product"])


@pytest.fixture
def parser_package():
    return cli.create_parser(["package"])


@pytest.fixture
def parser_completion():
    return cli.create_parser(["completion"])


@pytest.fixture
def args():
    return Namespace(
        command="",
        pattern=None,
        cache_file="fake-file-name",
        update_cache=False,
        no_cache=False,
    )

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

def test_parser_with_unknown_command(parser):
    """
    parser should exit if unknown command is provided
    """
    with pytest.raises(SystemExit):
        parser.parse_args(["foo_bad_command"])


def test_parser_with_known_commands(parser):
    """
    parser will not exit with known commands
    """
    args = parser.parse_args(["product"])
    assert args.command == "product"
    assert args.pattern == None
    args = parser.parse_args(["product", "pattern"])
    assert args.command == "product"
    assert args.pattern == "pattern"

    args = parser.parse_args(["product"])
    assert args.command == "product"
    assert args.pattern == None
    args = parser.parse_args(["product", "pattern"])
    assert args.command == "product"
    assert args.pattern == "pattern"


def test_parser_with_version_option(parser, capsys):
    with pytest.raises(SystemExit):
        parser.parse_args("--version".split())
    captured = capsys.readouterr()
    assert captured.out.strip() == f"pytest {__version__}"

    with pytest.raises(SystemExit):
        parser.parse_args("-v".split())
    captured = capsys.readouterr()
    assert captured.out.strip() == f"pytest {__version__}"


def test_parser_with_options_before_paramteter():
    """
    parser till not exit if options is before parameter
    """
    parser = cli.create_parser("--cache-file filename package 1234 vim".split())
    args = parser.parse_args("--cache-file filename package 1234 vim".split())
    assert args.cache_file == "filename"
    assert args.product == "1234"
    assert args.command == "package"
    assert args.pattern == "vim"

    parser = cli.create_parser(
        "--cache-file filename2 --update-cache product gvim".split()
    )
    args = parser.parse_args(
        "--cache-file filename2 --update-cache product gvim".split()
    )
    assert args.cache_file == "filename2"
    assert args.update_cache == True
    assert args.command == "product"
    assert args.pattern == "gvim"


def test_parser_cache_file(parser):
    """
    parser will not exit with match
    """
    args = parser.parse_args(["product"])
    assert args.cache_file == f"{str(Path.home())}/.cache/sps_cache.json"
    args = parser.parse_args(["product", "--cache-file", "testing"])
    assert args.cache_file == "testing"
    args = parser.parse_args(["product", "-C", "testing2"])
    assert args.cache_file == "testing2"


def test_parser_cache_age(parser):
    args = parser.parse_args(["product"])
    assert args.cache_age == 60
    args = parser.parse_args(["product", "--cache-age", "30"])
    assert args.cache_age == 30
    args = parser.parse_args(["product", "-a", "20"])
    assert args.cache_age == 20


def test_parser_product_command_update_cache(parser_product):
    """
    parser with product command --update-cache, false default
    """
    args = parser_product.parse_args("product --update-cache".split())
    assert args.cache_file == f"{str(Path.home())}/.cache/sps_cache.json"
    assert args.update_cache == True
    args = parser_product.parse_args("product -u".split())
    assert args.update_cache == True
    args = parser_product.parse_args(["product"])
    assert args.update_cache == False


def test_parser_product_command_no_cache(parser_product):
    """
    parser with product command --no-cache, false default
    """
    args = parser_product.parse_args("product --no-cache".split())
    assert args.no_cache == True
    args = parser_product.parse_args("product -N".split())
    assert args.no_cache == True
    args = parser_product.parse_args(["product"])
    assert args.no_cache == False


def test_parser_product_short(parser_product):
    args = parser_product.parse_args("product -s".split())
    assert args.command == "product"
    assert args.short == True

    args = parser_product.parse_args("product".split())
    assert args.command == "product"
    assert args.short == False

    args = parser_product.parse_args("product --short".split())
    assert args.command == "product"
    assert args.short == True


def test_parser_product_no_border(parser_product):
    args = parser_product.parse_args("product".split())
    assert args.no_borders == False
    args = parser_product.parse_args("product --no-borders".split())
    assert args.no_borders == True
    args = parser_product.parse_args("product -n".split())
    assert args.no_borders == True


def test_parser_product_sort_table(parser_product):
    args = parser_product.parse_args(["product"])
    assert args.sort_table == "id"
    for tn in ["id", "Name", "Edition", "Identifier", "Arch"]:
        args = parser_product.parse_args(f"product --sort-table {tn}".split())
        assert args.sort_table == tn
        args = parser_product.parse_args(f"product -S {tn}".split())
        assert args.sort_table == tn
    with pytest.raises(SystemExit):
        args = parser_product.parse_args(
            f"product --sort-table fake-column-name".split()
        )


def test_parser_product_no_header(parser_product):
    args = parser_product.parse_args("product".split())
    assert args.no_header == False
    args = parser_product.parse_args("product --no-header".split())
    assert args.no_header == True
    args = parser_product.parse_args("product -H".split())
    assert args.no_header == True


def test_parser_package_sort_table(parser_package):
    args = parser_package.parse_args("package fake".split())
    assert args.sort_table == "Name"
    for tn in ["Name", "Version", "Release", "Arch", "Module"]:
        args = parser_package.parse_args(f"package fake --sort-table {tn}".split())
        assert args.sort_table == tn
        args = parser_package.parse_args(f"package fake -S {tn}".split())
        assert args.sort_table == tn
    with pytest.raises(SystemExit):
        args = parser_package.parse_args(
            f"package fake --sort-table fake-column-name".split()
        )


def test_parser_package_no_border(parser_package):
    args = parser_package.parse_args("package test".split())
    assert args.no_borders == False
    args = parser_package.parse_args("package test --no-borders".split())
    assert args.no_borders == True
    args = parser_package.parse_args("package test -n".split())
    assert args.no_borders == True


def test_parser_package_no_header(parser_package):
    args = parser_package.parse_args("package test".split())
    assert args.no_header == False
    args = parser_package.parse_args("package test --no-header".split())
    assert args.no_header == True
    args = parser_package.parse_args("package test -H".split())
    assert args.no_header == True


def test_parser_package_command_product_id(parser_package):
    """
    parser with package command --product
    """
    args = parser_package.parse_args("package testing".split())
    assert args.cache_file == f"{str(Path.home())}/.cache/sps_cache.json"
    assert args.product == "testing"
    assert args.pattern == None
    args = parser_package.parse_args("package testing2 vim".split())
    assert args.product == "testing2"
    assert args.pattern == "vim"
    with pytest.raises(SystemExit):
        args = parser_package.parse_args("package".split())


def test_parser_package_command_exact_match(parser_package):
    args = parser_package.parse_args("package testing".split())
    assert args.exact_match == False
    args = parser_package.parse_args("package testing --exact-match".split())
    assert args.exact_match == True
    args = parser_package.parse_args("package testing -e".split())
    assert args.exact_match == True


def test_parser_completion(parser_completion):
    args = parser_completion.parse_args("completion".split())
    assert args.command == "completion"
    assert args.shell == None
    args = parser_completion.parse_args("completion bash".split())
    assert args.command == "completion"
    assert args.shell == "bash"


def test_main_product_output(mocker, capsys):
    class parser_proxy:
        def parse_args(self):
            return Namespace(
                command="product",
                pattern=None,
                cache_file="fake-file-name",
                update_cache=False,
                no_cache=False,
                short=False,
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


def test_main_product_output_short(mocker, capsys):
    class parser_proxy:
        def parse_args(self):
            return Namespace(
                command="product",
                pattern=None,
                cache_file="fake-file-name",
                update_cache=False,
                no_cache=False,
                short=True,
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

    output = "SLED/15.2/x86_64"

    cli.main()
    captured = capsys.readouterr()
    assert captured.out.strip() == output


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
                short=None,
                cache_file="fake-file-name",
                shell="bash",
                cache_age=60,
            )

    mocker.patch("sps.cache.age", autospec=True)
    cache.age.return_values={}
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
                short=True,
                no_borders=False,
                no_header=False,
                sort_table="id",
                cache_age=60
            )


    mocker.patch("sps.cli.create_parser", autospec=True)
    cli.create_parser.return_value = parser_proxy()
    mocker.patch("sps.products.get", autospec=True)
    products.get.return_value = data["product"]
    mocker.patch("sps.cache.age", autospec=True)
    cache.age.return_value = {}
    cli.main()
    cache.age.assert_called_once_with("fake-file-name", 60)
    cache.age.return_value = {"testing": "date"}
    cli.main()
    captured = capsys.readouterr()
    assert captured.err.strip() == "Warning: The testing cache is old, last updated date"

