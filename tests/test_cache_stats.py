import time

import pytest

import toolcache


cachetypes = ['memory', 'disk']


@pytest.mark.parametrize('cachetype', cachetypes)
def test_do_not_track_stats(cachetype):

    @toolcache.cache(cachetype, track_basic_stats=False)
    def f(a):
        return 2 * a

    assert f.cache.stats is None


@pytest.mark.parametrize('cachetype', cachetypes)
def test_track_basic_stats(cachetype):

    @toolcache.cache(cachetype, track_basic_stats=True)
    def f(a):
        return 2 * a

    target = {
        'n_hashes': 0,
        'n_checks': 0,
        'n_hits': 0,
        'n_misses': 0,
        'n_loads': 0,
        'n_saves': 0,
        'n_deletes': 0,
        'n_size_evictions': 0,
        'n_ttl_evictions': 0,
    }
    assert target == f.cache.stats

    f(1)
    target = {
        'n_hashes': 1,
        'n_checks': 1,
        'n_hits': 0,
        'n_misses': 1,
        'n_loads': 0,
        'n_saves': 1,
        'n_deletes': 0,
        'n_size_evictions': 0,
        'n_ttl_evictions': 0,
    }
    assert target == f.cache.stats

    f.cache.exists_in_cache(args=[1])
    target = {
        'n_hashes': 2,
        'n_checks': 2,
        'n_hits': 1,
        'n_misses': 1,
        'n_loads': 0,
        'n_saves': 1,
        'n_deletes': 0,
        'n_size_evictions': 0,
        'n_ttl_evictions': 0,
    }
    assert target == f.cache.stats

    f(1)
    target = {
        'n_hashes': 3,
        'n_checks': 3,
        'n_hits': 2,
        'n_misses': 1,
        'n_loads': 1,
        'n_saves': 1,
        'n_deletes': 0,
        'n_size_evictions': 0,
        'n_ttl_evictions': 0,
    }
    assert target == f.cache.stats

    f.cache.compute_entry_hash(args=[2])
    target = {
        'n_hashes': 4,
        'n_checks': 3,
        'n_hits': 2,
        'n_misses': 1,
        'n_loads': 1,
        'n_saves': 1,
        'n_deletes': 0,
        'n_size_evictions': 0,
        'n_ttl_evictions': 0,
    }
    assert target == f.cache.stats

    f(2)
    target = {
        'n_hashes': 5,
        'n_checks': 4,
        'n_hits': 2,
        'n_misses': 2,
        'n_loads': 1,
        'n_saves': 2,
        'n_deletes': 0,
        'n_size_evictions': 0,
        'n_ttl_evictions': 0,
    }
    assert target == f.cache.stats

    f.cache.delete_entry(2)
    target = {
        'n_hashes': 5,
        'n_checks': 4,
        'n_hits': 2,
        'n_misses': 2,
        'n_loads': 1,
        'n_saves': 2,
        'n_deletes': 1,
        'n_size_evictions': 0,
        'n_ttl_evictions': 0,
    }
    assert target == f.cache.stats


@pytest.mark.parametrize('cachetype', cachetypes)
def test_ttl_eviction_statistics(cachetype):

    @toolcache.cache(cachetype, track_basic_stats=True, ttl=1, max_size=3)
    def f(a):
        return 2 * a

    f(1)
    time.sleep(1)
    assert f.cache.get_cache_size() == 0
    assert f.cache.stats['n_ttl_evictions'] == 1


@pytest.mark.parametrize('cachetype', cachetypes)
def test_size_eviction_statistics(cachetype):

    @toolcache.cache(cachetype, track_basic_stats=True, max_size=3)
    def f(a):
        return 2 * a

    f(1)
    f(2)
    f(3)
    assert f.cache.get_cache_size() == 3
    assert f.cache.stats['n_size_evictions'] == 0
    f(4)
    assert f.cache.get_cache_size() == 3
    assert f.cache.stats['n_size_evictions'] == 1
    f(4)
    assert f.cache.get_cache_size() == 3
    assert f.cache.stats['n_size_evictions'] == 1
    f(1)
    assert f.cache.get_cache_size() == 3
    assert f.cache.stats['n_size_evictions'] == 2

