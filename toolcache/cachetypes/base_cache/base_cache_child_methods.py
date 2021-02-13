
class BaseCacheChildMethods:
    """abstract definitions of methods that implemented by child classes

    all cache features should work if these functions are implemented
    """

    def _save(self, entry_hash, entry_data):
        """save entry data to cache

        ## Inputs
        - entry_hash: hash of entry as computed by self.compute_entry_hash()
        - entry_data: data associated with entry
        """
        raise NotImplementedError('_save() not implemented')

    def _exists(self, entry_hash):
        """query whether entry exists in cache"""
        raise NotImplementedError('_entry_exists() not implemented')

    def _get_all(self):
        """get list of all entries in cache"""
        raise NotImplementedError('get_all_entry_hashes() not implemented')

    def _load(self, entry_hash):
        """load entry_data from cache"""
        raise NotImplementedError('_load() not implemented')

    def _delete(self, entry_hash):
        """remove single entry from cache"""
        raise NotImplementedError('_delete() not implemented')

