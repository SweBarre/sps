import pytest
import tempfile
import json
import os
import stat
from sps import cache


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


def test_cache_save_load(data):
    """
    saves and loads content from a file-like source
    """
    fn = tempfile.NamedTemporaryFile(delete=False)
    os.remove(fn.name)
    assert cache.save("product", fn.name, data["product"]) == None
    assert cache.load(fn.name) == data
    os.remove(fn.name)


def test_cache_save_bogus_data():
    """
    save will exit if bogus data provided
    """
    fn = tempfile.NamedTemporaryFile(delete=False)
    with pytest.raises(SystemExit):
        cache.save("product", fn.name, "{age:100}")
    os.remove(fn.name)


def test_cache_save_bogus_key():
    with pytest.raises(SystemExit):
        cache.save("fake-cache-key", "fake-file-name", [])


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
        cache.save("product", fn.name, data)
    os.remove(fn.name)


def test_cache_save_key_load_old(data):
    fn = tempfile.NamedTemporaryFile(delete=False)
    existing_data = {"testing": "testing", "product": "product"}
    with open(fn.name, "w") as f:
        json.dump(existing_data, f)

    cache.save("product", fn.name, data["product"])

    with open(fn.name, "r") as f:
        cachedata = json.load(f)

    new_data = {"testing": "testing", "product": data["product"]}

    assert new_data == cachedata


def test_cache_load_permission_denied(data):
    """
    load should exit the cache
    """
    fn = tempfile.NamedTemporaryFile(delete=False)
    os.remove(fn.name)
    cache.save("product", fn.name, data["product"])
    os.chmod(fn.name, stat.S_IWUSR)
    with pytest.raises(SystemExit):
        cache.load(fn.name)
    os.remove(fn.name)


def test_cache_lookup_product_found(data):
    """
    lookup will not exit if identifier is found
    """
    fn = tempfile.NamedTemporaryFile(delete=False)
    os.remove(fn.name)
    cache.save("product", fn.name, data["product"]) == None
    assert cache.lookup_product("SLED/15.2/x86_64", fn.name) == 1935
    os.remove(fn.name)


def test_cache_lookup_product_notfound(data):
    """
    lookup will exit if identifier is not found
    """
    fn = tempfile.NamedTemporaryFile(delete=False)
    os.remove(fn.name)
    cache.save("product", fn.name, data["product"]) == None
    with pytest.raises(SystemExit):
        cache.lookup_product("Bogus product name", fn.name)
    os.remove(fn.name)

def test_cache_age_warning_not_old(data):
    """
    
