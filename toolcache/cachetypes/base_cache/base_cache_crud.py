import time


class BaseCacheCRUD:
    """create, read, and delete operations for entries of BaseCache"""

    def save_entry(self, entry_hash, entry_data, verbose=None):
        """save entry data to cache

        ## Inputs
        - entry_hash: hash of entry as computed by self.compute_entry_hash()
        - entry_data: data associated with entry
        """

        with self.lock:

            # check max_size
            max_size = self.max_size
            if max_size is not None and self.get_cache_size() >= max_size:
                self.evict_to_size(max_size - 1)

            # print summary
            if verbose is None:
                verbose = self.verbose
            if verbose:
                self._print_save_summary(entry_hash)

            # save data to cache
            self._save(entry_hash=entry_hash, entry_data=entry_data)

            # track stats
            if self.stats is not None:
                self.stats['n_saves'] += 1
            if self.entry_creation_times is not None:
                self.entry_creation_times[entry_hash] = time.time()
            if self.entry_access_times is not None:
                self.entry_access_times[entry_hash] = time.time()
            if self.entry_access_counts is not None:
                self.entry_access_counts.setdefault(entry_hash, 0)

    def exists_in_cache(self, entry_hash=None, args=None, kwargs=None):
        """return whether entry exists in cache

        should specify either entry_hash, or at least one of args and kwargs

        ## Inputs
        - entry_hash: hash of entry
        - args: list of postitional args to use to compute hash
        - kwargs: list of keyword args to use to compute hash
        """

        # parse inputs
        if entry_hash is None:
            if args is None and kwargs is None:
                raise Exception('must specify entry_hash, or args and kwargs')
            if args is None:
                args = []
            if kwargs is None:
                kwargs = {}
            entry_hash = self.compute_entry_hash(args=args, kwargs=kwargs)

        # check whether exists
        exists = self._exists(entry_hash)

        # check ttl vs age
        if exists and self.entry_too_old(entry_hash):
            self.delete_entry(entry_hash)
            exists = False

        # track stats
        if self.stats is not None:
            with self.lock:
                self.stats['n_checks'] += 1
                if exists:
                    self.stats['n_hits'] += 1
                else:
                    self.stats['n_misses'] += 1

        return exists

    def get_all_entry_hashes(self):
        """get list of all hashes existing in cache"""
        return [
            entry_hash
            for entry_hash in self._get_all()
            if self.exists_in_cache(entry_hash)
        ]

    def get_cache_size(self):
        """query size of cache"""
        return len(self.get_all_entry_hashes())

    def load_entry(
        self,
        entry_hash=None,
        args=None,
        kwargs=None,
        verbose=None,
        must_exist=False,
    ):
        """load entry data from cache, or None if entry does not exist

        should specify either entry_hash, or at least one of args and kwargs

        ## Inputs
        - entry_hash: hash of entry as computed by self.compute_entry_hash()
        - args: list of postitional args to use to compute hash
        - kwargs: list of keyword args to use to compute hash
        - verbose: bool of whether to print loading, if None uses self.verbose
        - must_exist: bool of whether to raise exception if entry does not exist
        """

        # parse inputs
        if entry_hash is None:
            if args is None and kwargs is None:
                raise Exception('must specify entry_hash, or args and kwargs')
            if args is None:
                args = []
            if kwargs is None:
                kwargs = {}
            entry_hash = self.compute_entry_hash(args=args, kwargs=kwargs)

        with self.lock:
            if self.exists_in_cache(entry_hash):

                # print summary
                if verbose is None:
                    verbose = self.verbose
                if verbose:
                    self._print_load_summary(entry_hash)

                # load data
                entry_data = self._load(entry_hash)

                # track stats
                if self.stats is not None:
                    self.stats['n_loads'] += 1

            else:
                if must_exist:
                    raise Exception('entry does not exist in cache')
                else:
                    entry_data = None

            # track stats
            if self.entry_access_times is not None:
                self.entry_access_times[entry_hash] = time.time()
            if self.entry_access_counts is not None:
                self.entry_access_counts.setdefault(entry_hash, 0)
                self.entry_access_counts[entry_hash] += 1

            return entry_data

    def delete_entry(self, entry_hash=None, args=None, kwargs=None):
        """delete entry from cache

        should specify either entry_hash, or at least one of args and kwargs

        ## Inputs
        - entry_hash: hash of entry as computed by self.compute_entry_hash()
        - args: list of postitional args to use to compute hash
        - kwargs: list of keyword args to use to compute hash
        """

        if entry_hash is None:
            if args is None and kwargs is None:
                raise Exception('must specify entry_hash, or args and kwargs')
            if args is None:
                args = []
            if kwargs is None:
                kwargs = {}
            entry_hash = self.compute_entry_hash(args=args, kwargs=kwargs)

        with self.lock:
            self._delete(entry_hash)
            if self.stats is not None:
                self.stats['n_deletes'] += 1

    def delete_all_entries(self):
        """delete all entries from cache"""
        with self.lock:
            size = self.get_cache_size()
            self._delete_all()
            if self.stats is not None:
                self.stats['n_deletes'] += size

    def _delete_all(self):
        """clear all cache entries

        this method can be reimplemented by child classes for better performance
        """
        for entry_hash in self.get_all_entry_hashes():
            self.delete_entry(entry_hash)

    #
    # # introspection
    #

    def _print_load_summary(self, entry_hash):
        """print summary about entry being loaded"""
        print('[cache]', self.cache_name, 'loading from cache')

    def _print_save_summary(self, entry_hash):
        """print summary about entry being saved"""
        print('[cache]', self.cache_name, 'saving to cache')

