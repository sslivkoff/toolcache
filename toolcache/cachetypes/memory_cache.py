"""class specifying a cache that stores entries in memory using a dict"""

import time

from . import base_cache


class MemoryCache(base_cache.BaseCache):
    """a MemoryCache is a cache that stores its entries in a simple dict"""

    def __init__(self, **super_kwargs):
        self.cache = {}
        super().__init__(**super_kwargs)

    def _save(self, entry_hash, entry_data):
        self.cache[entry_hash] = entry_data
        if self.entry_creation_times is not None:
            self.entry_creation_times[entry_hash] = time.time()

    def _exists(self, entry_hash):
        return entry_hash in self.cache

    def _get_all(self):
        return list(self.cache.keys())

    def _load(self, entry_hash):
        if self.entry_access_times is not None:
            self.entry_access_times[entry_hash] = time.time()
        return self.cache[entry_hash]

    def _delete(self, entry_hash):
        if entry_hash in self.cache:
            del self.cache[entry_hash]

    def _delete_all(self):
        self.cache = {}

