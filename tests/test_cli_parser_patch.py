import pytest
from argparse import ArgumentParser, Namespace
from sps import patch, cli


@pytest.fixture
def parser():
    return cli.create_parser(["patch"])


def test_parser_patch_______(parser):
    """
    parser with patch command
    """
    pass
