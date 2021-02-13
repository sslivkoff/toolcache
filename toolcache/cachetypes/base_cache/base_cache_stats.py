import time


class BaseCacheStats:
    def _initialize_cache_stats(
        self,
        track_basic_stats,
        track_detailed_stats,
        track_creation_times,
        track_access_times,
        track_access_counts,
    ):

        # initialize basic stats
        if track_basic_stats:
            self.stats = {
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
        else:
            self.stats = None

        if self.ttl is not None:
            if track_creation_times is not None and not track_creation_times:
                raise Exception('must track creation times if using ttl policy')
            track_creation_times = True

        # creation times
        if track_creation_times is None:
            if self.max_size_policy == 'fifo':
                track_creation_times = None
            else:
                track_creation_times = track_detailed_stats
        if track_creation_times:
            self.entry_creation_times = {}
        else:
            if self.max_size_policy == 'fifo':
                raise Exception('must track_access_times if using fifo')
            self.entry_creation_times = None
        self.track_creation_times = track_creation_times

        # access times
        if track_access_times is None:
            if self.max_size_policy == 'lru':
                track_access_times = True
            else:
                track_access_times = track_detailed_stats
        if track_access_times:
            self.entry_access_times = {}
        else:
            if self.max_size_policy == 'lru':
                raise Exception('must track_access_times if using lru')
            self.entry_access_times = None
        self.track_access_times = track_access_times

        # access counts
        if track_access_counts is None:
            if self.max_size_policy == 'lfu':
                track_access_counts = True
            else:
                track_access_counts = track_detailed_stats
        if track_access_counts:
            self.entry_access_counts = {}
        else:
            if self.max_size_policy == 'lfu':
                raise Exception('must track_access_counts if using lfu')
            self.entry_access_counts = None
        self.track_access_counts = track_access_counts

    def get_entry_creation_time(self, entry_hash):
        """get creation time of an individual entry"""
        if self.track_creation_times is None:
            raise Exception('not tracking entry creation times')
        return self.entry_creation_times[entry_hash]

    def get_all_entry_creation_times(self, must_exist=True):
        """get creation times of all entries"""
        if self.track_creation_times is None:
            raise Exception('not tracking entry creation times')
        creation_times = self.entry_creation_times
        if must_exist:
            return {
                entry_hash: creation_times[entry_hash]
                for entry_hash in self.get_all_entry_hashes()
            }
        else:
            return creation_times

    def get_entry_age(self, entry_hash):
        """get age of an individual entry"""
        if self.track_creation_times is None:
            raise Exception('not tracking entry creation times')
        return time.time() - self.entry_creation_times[entry_hash]

    def get_all_entry_ages(self, must_exist=True):
        """get ages of all entries"""
        if self.track_creation_times is None:
            raise Exception('not tracking entry creation times')
        creation_times = self.entry_creation_times
        if must_exist:
            return {
                entry_hash: time.time() - creation_times[entry_hash]
                for entry_hash in self.get_all_entry_hashes()
            }
        else:
            return {
                entry_hash: time.time() - creation_time
                for entry_hash, creation_time in creation_times.items()
            }

    def get_entry_access_time(self, entry_hash):
        """get access count for an individual entry"""
        if self.track_access_times is None:
            raise Exception('not tracking entry access times')
        return self.entry_access_times[entry_hash]

    def get_all_entry_access_times(self, must_exist=True):
        """get access times for all entries"""
        if self.track_access_times is None:
            raise Exception('not tracking entry access times')
        access_times = self.entry_access_times
        if must_exist:
            return {
                entry_hash: access_times[entry_hash]
                for entry_hash in self.get_all_entry_hashes()
            }
        else:
            return access_times

    def get_entry_access_count(self, entry_hash):
        """get access count for an individual entry"""
        if self.track_access_counts is None:
            raise Exception('not tracking entry access counts')
        return self.entry_access_times[entry_hash]

    def get_all_entry_access_counts(self, must_exist=True):
        """get access counts for all entries"""
        if self.track_access_counts is None:
            raise Exception('not tracking entry access counts')
        access_counts = self.entry_access_counts
        if must_exist:
            return {
                entry_hash: access_counts[entry_hash]
                for entry_hash in self.get_all_entry_hashes()
            }
        else:
            return access_counts

    def print_cache_stats(self):
        """print stats related to cache"""

        print('stats for cache', self.cache_name)
        print('current state:')
        print('    - n_entries:', self.get_cache_size())
        print('    - ttl:', self.ttl)
        print('    - max_size:', self.max_size)
        print('    - max_size_policy:', self.max_size_policy)
        print('usage:')
        if self.stats is not None:
            for key, value in self.stats.items():
                print('    - ' + key + ':', value)
        else:
            print('[basic usage stats not being tracked]')

        if self.track_creation_times is not None:
            print(
                '- '
                + str(len(self.track_creation_times))
                + ' creation_times being tracked '
                + 'see cache attribute `track_creation_times`'
            )
        if self.track_access_times is not None:
            print(
                '- '
                + str(len(self.track_access_times))
                + ' access_times being tracked '
                + 'see cache attribute `track_access_times`'
            )
        if self.track_access_counts is not None:
            print(
                '- '
                + str(len(self.track_access_counts))
                + ' access_counts being tracked '
                + 'see cache attribute `track_access_counts`'
            )

