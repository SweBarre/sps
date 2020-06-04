import pytest
import tempfile
import json
import os
import stat
from sps import cache


@pytest.fixture
def data():
    return {
        "data": [
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


def test_cache_save_load(data):
    """
    saves and loads content from a file-like source
    """
    fn = tempfile.NamedTemporaryFile(delete=False)
    assert cache.save(fn.name, data) == None
    assert cache.load(fn.name) == data
    os.remove(fn.name)


def test_cache_save_bougus_data():
    """
    save will exit if bogus data provided
    """
    fn = tempfile.NamedTemporaryFile(delete=False)
    with pytest.raises(SystemExit):
        cache.save(fn.name, "{age:100}")
    os.remove(fn.name)


def test_cache_load_bougus_data():
    """
    load will exit if bogus data provided
    """
    fn = tempfile.NamedTemporaryFile(delete=False)
    with open(fn.name, "w") as f:
        f.write("lsdkjfalskdjf")
    with pytest.raises(SystemExit):
        cache.load(fn.name)
    os.remove(fn.name)


def test_cache_save_permission_denied(data):
    """
    save should exit the cache
    """
    fn = tempfile.NamedTemporaryFile(delete=False)
    os.chmod(fn.name, stat.S_IRUSR)
    with pytest.raises(SystemExit):
        cache.save(fn.name, data)
    os.remove(fn.name)


def test_cache_load_permission_denied(data):
    """
    load should exit the cache
    """
    fn = tempfile.NamedTemporaryFile(delete=False)
    cache.save(fn.name, data)
    os.chmod(fn.name, stat.S_IWUSR)
    with pytest.raises(SystemExit):
        cache.load(fn.name)
    os.remove(fn.name)


def test_cache_lookup_found(data):
    """
    lookup will not exit if identifier is found
    """
    fn = tempfile.NamedTemporaryFile(delete=False)
    cache.save(fn.name, data) == None
    assert cache.lookup("SLED/15.2/x86_64", fn.name) == 1935
    os.remove(fn.name)


def test_cache_lookup_notfound(data):
    """
    lookup will exit if identifier is not found
    """
    fn = tempfile.NamedTemporaryFile(delete=False)
    cache.save(fn.name, data) == None
    with pytest.raises(SystemExit):
        cache.lookup("Bogus product name", fn.name)
    os.remove(fn.name)
