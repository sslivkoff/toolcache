import json
import tempfile

import toolcache


def test_persistence_of_disk_cache():
    cache_dir = tempfile.mkdtemp()

    @toolcache.cache('disk', cache_dir=cache_dir)
    def f(a, b, c):
        return (a, b, c)

    f(1, 2, 3)
    assert f.cache.get_cache_size() == 1
    f(1, 2, 3)
    assert f.cache.get_cache_size() == 1
    f(4, 5, 6)
    assert f.cache.get_cache_size() == 2

    @toolcache.cache('disk', cache_dir=cache_dir)
    def f(a, b, c):
        return (a, b, c)

    assert f.cache.get_cache_size() == 2
    f(1, 2, 3)
    assert f.cache.get_cache_size() == 2
    f(1, 2, 3)
    assert f.cache.get_cache_size() == 2
    f(4, 5, 6)
    assert f.cache.get_cache_size() == 2
    f(7, 8, 9)


def test_custom_disk_io_functions():

    def f_disk_save(cache_path, entry_data):
        with open(cache_path, 'w') as f:
            json.dump(entry_data, f)

    def f_disk_load(cache_path):
        with open(cache_path, 'w') as f:
            json.load(f)

    @toolcache.cache('disk', f_disk_save=f_disk_save, f_disk_load=f_disk_load)
    def f(a, b, c):
        return [a, b, c]

