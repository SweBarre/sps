import pytest
from sps.helpers import print_warn, print_err, line_format, CWARNING, CERROR, CRESET


@pytest.fixture
def data():
    return [
        "989374",
        "1041710",
        "1006780",
        "asdfasdfasfd",
        "sdff",
        "dsdf",
        "sdfadfsfasdfasfasdfasdfasfdsadfsda",
        "dsfsdf",
    ]


def test_print_warn(capsys):
    print_warn("testing")
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err.strip() == f"{CWARNING}Warning:{CRESET} testing"


def test_print_err(capsys):
    print_err("testing")
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err.strip() == f"{CERROR}Error:{CRESET} testing"


def test_line_format(data):
    assert (
        line_format(data)
        == "989374 1041710 1006780 asdfasdfasfd sdff dsdf sdfadfsfasdfasfasdfasdfasfdsadfsda\ndsfsdf"
    )


def test_line_format_indent(data):
    assert (
        line_format(data, indent=2)
        == "  989374 1041710 1006780 asdfasdfasfd sdff dsdf sdfadfsfasdfasfasdfasdfasfdsadfsda\n  dsfsdf"
    )


def test_line_format_length(data):
    assert (
        line_format(data, length=7)
        == "989374 1041710\n1006780\nasdfasdfasfd\nsdff dsdf\nsdfadfsfasdfasfasdfasdfasfdsadfsda\ndsfsdf"
    )


def test_list_format_lenght_indent(data):
    assert (
        line_format(data, indent=2, length=7)
        == "  989374\n  1041710\n  1006780\n  asdfasdfasfd\n  sdff dsdf\n  sdfadfsfasdfasfasdfasdfasfdsadfsda\n  dsfsdf"
    )
