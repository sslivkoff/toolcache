import pytest

import toolcache


cachetypes = [toolcache.MemoryCache, toolcache.DiskCache]


@pytest.mark.parametrize('Cachetype', cachetypes)
def test_standalone_cache(Cachetype):

    cache = Cachetype()

    entry_hash = cache.compute_entry_hash(args=[1])
    entry_data = 'test message'

    cache.save_entry(entry_hash=entry_hash, entry_data=entry_data)
    assert cache.get_cache_size() == 1

    loaded_entry_data = cache.load_entry(entry_hash=entry_hash)
    assert loaded_entry_data == entry_data

    cache.save_entry(entry_hash=entry_hash, entry_data=entry_data)
    assert cache.get_cache_size() == 1

    cache.save_entry(entry_hash=entry_hash, entry_data='other data')
    assert cache.get_cache_size() == 1

    loaded_entry_data = cache.load_entry(entry_hash=entry_hash)
    assert loaded_entry_data != entry_data

