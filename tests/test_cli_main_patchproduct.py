import pytest
from argparse import Namespace
from sps import cache, patchproducts, cli


@pytest.fixture
def data():
    return [
        {
            "name": "Legacy Module",
            "version": "15 SP2",
            "architecture": "aarch64",
            "id": "Legacy_Module/15_SP2/aarch64",
        },
        {
            "name": "SUSE Linux Enterprise Server for SAP Applications",
            "version": "15 SP2",
            "architecture": "x86_64",
            "id": "SUSE_Linux_Enterprise_Server_for_SAP_Applications/15_SP2/x86_64",
        },
        {
            "name": "SUSE Linux Enterprise Real Time Extension",
            "version": "12 SP1",
            "architecture": "x86_64",
            "id": "SUSE_Linux_Enterprise_Real_Time_Extension/12_SP1/x86_64",
        },
        {
            "name": "Development Tools Module",
            "version": "15",
            "architecture": "s390x",
            "id": "Development_Tools_Module/15/s390x",
        },
    ]


@pytest.fixture
def parser():
    class P:
        command = "patchproduct"
        pattern = None
        cache_file = "fake-file-name"
        update_cache = False
        no_cache = False
        short = False
        no_borders = False
        no_header = False
        sort_table = "Name"
        cache_age = 60

        def parse_args(self):
            return Namespace(
                command=self.command,
                pattern=self.pattern,
                cache_file=self.cache_file,
                update_cache=self.update_cache,
                no_cache=self.no_cache,
                short=self.short,
                no_borders=self.no_borders,
                no_header=self.no_header,
                sort_table=self.sort_table,
                cache_age=self.cache_age,
            )

    return P


def test_main_patchproduct_output(parser, data, mocker, capsys):
    mocker.patch("sps.cache.age")
    cache.age.return_value = {}
    mocker.patch("sps.patchproducts.get")
    patchproducts.get.return_value = data
    mocker.patch("sps.cli.create_parser")
    p = parser()
    cli.create_parser.return_value = p
    output = """+---------------------------------------------------+---------+---------+
| Name                                              | Version | Arch    |
+---------------------------------------------------+---------+---------+
| Development Tools Module                          | 15      | s390x   |
| Legacy Module                                     | 15 SP2  | aarch64 |
| SUSE Linux Enterprise Real Time Extension         | 12 SP1  | x86_64  |
| SUSE Linux Enterprise Server for SAP Applications | 15 SP2  | x86_64  |
+---------------------------------------------------+---------+---------+
"""
    cli.main()
    captured = capsys.readouterr()
    assert captured.out == output
