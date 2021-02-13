import time

import pytest

import toolcache


cachetypes = ['memory', 'disk']


@pytest.mark.parametrize('cachetype', cachetypes)
def test_lru_cache(cachetype):

    @toolcache.cache(cachetype, max_size=3, max_size_policy='lru')
    def f(a):
        return a * 2

    f(1)
    f(2)
    f(3)
    assert f.cache.get_cache_size() == 3

    f(4)
    assert f.cache.get_cache_size() == 3

    input_hashes = {f.cache.f_hash(input) for input in {2, 3, 4}}
    assert set(f.cache.get_all_entry_hashes()) == input_hashes

    f(4)
    assert f.cache.get_cache_size() == 3

    f(1)
    assert f.cache.get_cache_size() == 3
    input_hashes = {f.cache.f_hash(input) for input in {1, 3, 4}}
    assert set(f.cache.get_all_entry_hashes()) == input_hashes


@pytest.mark.parametrize('cachetype', cachetypes)
def test_lfu_cache(cachetype):

    @toolcache.cache(cachetype, max_size=3, max_size_policy='lfu')
    def f(a):
        return a * 2

    f(1)
    f(2)
    f(3)
    assert f.cache.get_cache_size() == 3

    f(1)
    f(1)
    f(1)
    f(2)
    f(2)

    f(4)
    assert f.cache.get_cache_size() == 3
    input_hashes = {f.cache.f_hash(input) for input in {1, 2, 4}}
    assert set(f.cache.get_all_entry_hashes()) == input_hashes

    f(4)
    f(4)
    f(4)
    f(4)
    f(4)
    f(2)
    f(2)
    f(2)
    f(2)

    f(3)

    assert f.cache.get_cache_size() == 3
    input_hashes = {f.cache.f_hash(input) for input in {2, 3, 4}}
    assert set(f.cache.get_all_entry_hashes()) == input_hashes


@pytest.mark.parametrize('cachetype', cachetypes)
def test_fifo_cache(cachetype):

    @toolcache.cache(cachetype, max_size=3, max_size_policy='fifo')
    def f(a):
        return a * 2

    f(1)
    f(2)
    f(3)
    assert f.cache.get_cache_size() == 3
    f(4)
    assert f.cache.get_cache_size() == 3
    input_hashes = {f.cache.f_hash(input) for input in {2, 3, 4}}
    f(4)
    assert f.cache.get_cache_size() == 3
    input_hashes = {f.cache.f_hash(input) for input in {2, 3, 4}}
    f(2)
    f(5)
    assert f.cache.get_cache_size() == 3
    input_hashes = {f.cache.f_hash(input) for input in {3, 4, 5}}
    f(1)
    assert f.cache.get_cache_size() == 3
    input_hashes = {f.cache.f_hash(input) for input in {1, 4, 5}}


@pytest.mark.parametrize('cachetype', cachetypes)
def test_lru_default_cache(cachetype):

    @toolcache.cache(cachetype, max_size=3)
    def f(a):
        return a * 2

    f(1)
    f(2)
    f(3)
    assert f.cache.get_cache_size() == 3

    f(4)
    assert f.cache.get_cache_size() == 3

    input_hashes = {f.cache.f_hash(input) for input in {2, 3, 4}}
    assert set(f.cache.get_all_entry_hashes()) == input_hashes

    f(4)
    assert f.cache.get_cache_size() == 3

    f(1)
    assert f.cache.get_cache_size() == 3
    input_hashes = {f.cache.f_hash(input) for input in {1, 3, 4}}
    assert set(f.cache.get_all_entry_hashes()) == input_hashes


@pytest.mark.parametrize('cachetype', cachetypes)
def test_ttl(cachetype):

    @toolcache.cache(cachetype, ttl=1)
    def f(a):
        return a * 2

    entry_hash = f.cache.f_hash(1)

    f(1)
    assert f.cache.exists_in_cache(entry_hash)
    f(1)
    assert f.cache.exists_in_cache(entry_hash)
    time.sleep(1)
    assert not f.cache.exists_in_cache(entry_hash)

