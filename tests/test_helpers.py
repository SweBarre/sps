from sps import helpers

def test_print_warn(capsys):
    helpers.print_warn("testing")
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err.strip() == f"{helpers.CWARNING}Warning:{helpers.CRESET} testing"


def test_print_err(capsys):
    helpers.print_err("testing")
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err.strip() == f"{helpers.CERROR}Error:{helpers.CRESET} testing"
