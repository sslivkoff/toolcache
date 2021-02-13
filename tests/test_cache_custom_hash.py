import pytest

import toolcache


cachetypes = ['memory', 'disk']


@pytest.mark.parametrize('cachetype', cachetypes)
def test_custom_f_hash(cachetype):

    def f_hash(a):
        if a in [1, 2, 3]:
            return 'custom'
        else:
            return str(a)

    @toolcache.cache(cachetype, f_hash=f_hash)
    def f(a):
        return 2 * a

    result1 = f(1)
    assert f.cache.get_cache_size() == 1
    result2 = f(2)
    assert f.cache.get_cache_size() == 1
    assert result2 == result1
    result3 = f(3)
    assert f.cache.get_cache_size() == 1
    assert result3 == result1
    result3 = f(4)
    assert f.cache.get_cache_size() == 2
    assert result3 != result1


@pytest.mark.parametrize('cachetype', cachetypes)
def test_custom_f_hash_multiple_args(cachetype):

    def f_hash(a, b):
        if a in [1, 2, 3]:
            return 'custom'
        else:
            return str([a, b])

    @toolcache.cache(cachetype, f_hash=f_hash)
    def f(a, b):
        return [2 * a, 3 * b]

    result1 = f(1, 1)
    assert f.cache.get_cache_size() == 1
    result2 = f(2, 1)
    assert f.cache.get_cache_size() == 1
    assert result2 == result1
    result3 = f(3, 1)
    assert f.cache.get_cache_size() == 1
    assert result3 == result1
    result3 = f(4, 1)
    assert f.cache.get_cache_size() == 2
    assert result3 != result1

    result1 = f(1, 2)
    assert f.cache.get_cache_size() == 2
    result2 = f(2, 2)
    assert f.cache.get_cache_size() == 2
    assert result2 == result1
    result3 = f(3, 2)
    assert f.cache.get_cache_size() == 2
    assert result3 == result1
    result3 = f(4, 1)
    assert f.cache.get_cache_size() == 2
    assert result3 != result1
    result3 = f(4, 2)
    assert f.cache.get_cache_size() == 3
    assert result3 != result1

