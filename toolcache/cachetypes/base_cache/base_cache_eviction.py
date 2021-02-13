import types

import tooltime


class BaseCacheEviction:
    def _initialize_eviction_policies(
        self,
        ttl,
        max_size,
        max_size_policy,
    ):
        """initialize cache attributes related to eviction and stat tracking

        see BaseCache.__init__ docstring for full description of each argument
        """

        # set ttl
        if isinstance(ttl, str):
            ttl = tooltime.timelength_label_to_seconds(ttl)
        self.ttl = ttl

        # set size limits and policy
        self.max_size = max_size
        if self.max_size is None:
            self.max_size_policy = None
        else:
            if max_size_policy is None:
                max_size_policy = 'lru'
            if isinstance(max_size_policy, types.FunctionType):
                self.max_size_policy = 'custom'
                self.get_cache_eviction = max_size_policy
            elif isinstance(max_size_policy, str):
                max_size_policy = max_size_policy.lower()
                if max_size_policy == 'lru':
                    self.max_size_policy = max_size_policy
                    self.get_cache_eviction = self.get_lru_eviction
                elif max_size_policy == 'fifo':
                    self.max_size_policy = max_size_policy
                    self.get_cache_eviction = self.get_fifo_eviction
                elif max_size_policy == 'lfu':
                    self.max_size_policy = max_size_policy
                    self.get_cache_eviction = self.get_lfu_eviction
                else:
                    raise Exception('max_size_policy: ' + str(max_size_policy))
            else:
                raise Exception('max_size_policy: ' + str(max_size_policy))

    def entry_too_old(self, entry_hash):
        """return whether entry_hash satisfies ttl and delete it if too old"""
        if self.ttl is None:
            return False
        if self.get_entry_age(entry_hash) >= self.ttl:
            if self.verbose:
                print('[cache]', self.cache_name, 'evicting old entry')
            with self.lock:
                self.delete_entry(entry_hash)
                if self.stats is not None:
                    self.stats['n_ttl_evictions'] += 1
            return True
        else:
            return False

    def evict_to_size(self, target_size):
        """remove items from cache until cache reaches target size"""

        with self.lock:
            print(self.get_cache_size)

            # compute number to evict
            n_to_evict = self.get_cache_size() - target_size
            if n_to_evict < 1:
                return

            # evict hashes
            for e in range(n_to_evict):
                entry_hash = self.get_cache_eviction()
                print("PEROFMRING DELETE", entry_hash)
                self.delete_entry(entry_hash)
                if self.stats is not None:
                    self.stats['n_size_evictions'] += 1

            print(self.get_cache_size)

    #
    # # specific eviction algorithms
    #

    def get_lru_eviction(self):
        """determine which entries to evict using lru algorithm"""
        access_times = self.get_all_entry_access_times(must_exist=True)
        _, entry_hash = min(zip(access_times.values(), access_times.keys()))
        return entry_hash

    def get_fifo_eviction(self):
        """determine which entries to evict using fifo algorithm"""
        ages = self.get_all_entry_ages(must_exist=True)
        _, entry_hash = max(zip(ages.values(), ages.keys()))
        return entry_hash

    def get_lfu_eviction(self):
        """determine which entries to evict using lfu algorithm"""
        access_counts = self.get_all_entry_access_counts(must_exist=True)
        _, entry_hash = min(zip(access_counts.values(), access_counts.keys()))
        return entry_hash

