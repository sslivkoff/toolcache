"""toolcache can save caches to disk

use cases include:
- the cache needs to be persistent
- the cache is too large to fit in memory

use `f_disk_save` and `f_disk_load` to control how cache data is saved to disk
"""

import toolcache


#
# # cache to persistent folder
#

@toolcache.cache('disk', cache_dir='/path/to/dir')
def cache_to_persistent_dir(a, b, c):
    """this cache will be persistent across machine restarts

    if cache_dir is not specified, will instead cache to a tmpdir
    """
    return a * b * c


#
# # cache with custom disk io
#

import numpy as np


def save_numpy_array(entry_path, entry_data):
    np.savez_compressed(entry_path, entry_data)


def load_numpy_array(entry_path):
    np.load(entry_path)


@toolcache.cache(
    'disk',
    f_disk_save=save_numpy_array,
    f_disk_load=load_numpy_array,
)
def f(a, b, c):
    """this function will now efficiently cache numpy arrays to disk"""

    # an expensive computation, or maybe loading from network
    array = some_expensive_operation(a, b, c)
    return array

