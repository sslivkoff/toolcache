import pytest

import toolcache


cachetypes = ['memory', 'disk']


@pytest.mark.parametrize('cachetype', cachetypes)
def test_create_standalone_instance(cachetype):

    CacheClass = toolcache.get_cache_class(cachetype)
    cache = CacheClass()

    entry_hash = 4
    entry_data = 27

    cache.save_entry(entry_hash=entry_hash, entry_data=entry_data)
    loaded_data = cache.load_entry(entry_hash=entry_hash)
    assert loaded_data == entry_data


@pytest.mark.parametrize('cachetype', cachetypes)
def test_function_get_cache_instance(cachetype):
    @toolcache.cache(cachetype=cachetype)
    def test_function(a, b, c):
        return a * b * c

    cache_instance = test_function.cache
    assert isinstance(cache_instance, toolcache.BaseCache)


@pytest.mark.parametrize('cachetype', cachetypes)
def test_method_get_cache_size(cachetype):
    @toolcache.cache(cachetype=cachetype)
    def test_function(a, b, c):
        return a * b * c

    cache_instance = test_function.cache
    assert cache_instance.get_cache_size() == 0
    test_function(1, 2, 3)
    assert cache_instance.get_cache_size() == 1
    test_function(1, 2, 3)
    assert cache_instance.get_cache_size() == 1
    test_function(1, 2, 4)
    assert cache_instance.get_cache_size() == 2
    test_function(1, 2, 4)
    assert cache_instance.get_cache_size() == 2
    test_function(1, 2, 5)
    assert cache_instance.get_cache_size() == 3


@pytest.mark.parametrize('cachetype', cachetypes)
def test_method_delete_all_entries(cachetype):
    @toolcache.cache(cachetype=cachetype)
    def test_function(a, b, c):
        return a * b * c

    test_function(1, 2, 3)
    test_function(1, 2, 4)
    test_function(1, 2, 5)
    cache_instance = test_function.cache
    assert cache_instance.get_cache_size() == 3
    cache_instance.delete_all_entries()
    assert cache_instance.get_cache_size() == 0


