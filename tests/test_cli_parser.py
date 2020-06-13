import pytest
from argparse import ArgumentParser, Namespace
from prettytable import PrettyTable
import prettytable
from pathlib import Path
from sps import helpers, cli, products, packages, completion, cache, __version__


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
def parser_patchproduct():
    return cli.create_parser(["patchproduct"])


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

    args = parser.parse_args(["patchproduct", "pattern"])
    assert args.command == "patchproduct"
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


def test_parser_patchproducts(parser_patchproduct):
    args = parser_patchproduct.parse_args(["patchproduct"])
    assert args.command == "patchproduct"
    assert args.pattern == None
    args = parser_patchproduct.parse_args("patchproduct testing".split())
    assert args.command == "patchproduct"
    assert args.pattern == "testing"
