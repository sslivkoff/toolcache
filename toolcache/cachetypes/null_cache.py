from . import base_cache


class NullCache(base_cache.BaseCache):
    """a NullCache cache that does not save or load any entries

    useful for programmatically controlling whether a function has a cache
    """

    def __init__(self, **super_kwargs):
        super_kwargs.setdefault('track_detailed_stats', False)
        super_kwargs.setdefault('track_creation_times', False)
        super_kwargs.setdefault('track_access_times', False)
        super_kwargs.setdefault('track_access_counts', False)
        super().__init__(**super_kwargs)

    def _save(self, entry_hash, entry_data):
        pass

    def _exists(self, entry_hash):
        return False

    def _load(self, entry_hash):
        return None

    def _delete(self, entry_hash):
        pass

    def get_all_entry_hashes(self):
        return []

    def compute_entry_hash(self, args, kwargs):
        return ''

