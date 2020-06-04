import os
import pytest
from sps import completion


def test_completion_bash():
    assert "/path/to/cache/file" in completion.get("/path/to/cache/file", "bash")


def test_completion_environment():
    os.environ["SHELL"] = "/bin/bash"
    assert "/path/to/cache/file" in completion.get("/path/to/cache/file")
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
