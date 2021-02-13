import contextlib
import threading
import multiprocessing
import uuid

from . import base_cache_crud
from . import base_cache_child_methods
from . import base_cache_eviction
from . import base_cache_hash
from . import base_cache_stats


class BaseCache(
    base_cache_crud.BaseCacheCRUD,
    base_cache_child_methods.BaseCacheChildMethods,
    base_cache_eviction.BaseCacheEviction,
    base_cache_hash.BaseCacheHash,
    base_cache_stats.BaseCacheStats,
):
    """BaseCache is an abstract class that cache implementations inherit from

    BaseCache is defined across multiple files using mixins for readability
    """

    def __init__(
        self,
        safety='thread',
        verbose=False,
        cache_name=None,
        old_f=None,
        hash_mode=None,
        f_hash=None,
        normalize_hash_inputs=None,
        hash_include_args=None,
        hash_exclude_args=None,
        ttl=None,
        max_size=None,
        max_size_policy=None,
        track_basic_stats=True,
        track_detailed_stats=False,
        track_creation_times=None,
        track_access_times=None,
        track_access_counts=None,
    ):
        """initialize cache

        ## Inputs

        #### Miscellaneous Options
        - safety: one of ['thread', 'process', None] for concurrency safety
        - verbose: bool of whether to be verbose
        - cache_name: str name of cache, used in verbose reporting statements
        - old_f: function being decorated by cache, None for standalone cache

        #### Hash Options
        - hash_mode: str of hash mode, either 'json' or 'json_digest'
        - f_hash: function for computing hash
            - should take same args as decorated function
        - normalize_hash_inputs: bool of whether to normalize function args
            - if f() has one arg, g, then normalizing will make f(5) == f(g=5)
              according to the hashes computed by the hash
        - hash_include_args: list of str names of arguments used to compute hash
            - this requires normalizing hash inputs
        - hash_exclude_args: list of str names of arguments excluded from hash
            - this requires normalizing hash inputs

        #### Eviction Options
        - ttl: Timelength of maximum age of entries in cache
        - max_size: int count of maximum number of entries in cache
        - max_size_policy: one of ['lru', 'fifo', 'lfu', None]

        #### Statistic Tracking Options
        - track_basic_stats: bool of whether to track basic usage stats
        - track_detailed_stats: bool of whether to track creations and accesses
        - track_creation_times: bool of whether to track creation times
        - track_access_times: bool of whether to track access times
        - track_access_counts: bool of whether to track access counts
        """

        # set verbosity and name
        self.verbose = verbose
        if cache_name is not None:
            self.cache_name = cache_name
        else:
            if old_f is not None:
                self.cache_name = old_f.__name__
            else:
                self.cache_name = uuid.uuid4().hex

        # initialize eviction policies
        self._initialize_eviction_policies(
            ttl=ttl,
            max_size=max_size,
            max_size_policy=max_size_policy,
        )

        # initialize stats
        self._initialize_cache_stats(
            track_basic_stats=track_basic_stats,
            track_detailed_stats=track_detailed_stats,
            track_creation_times=track_creation_times,
            track_access_times=track_access_times,
            track_access_counts=track_access_counts,
        )

        # initialize thread or process lock
        self._initialize_context_lock(safety=safety)

        # initialize hash config
        self._initialize_hash_config(
            old_f=old_f,
            hash_mode=hash_mode,
            normalize_hash_inputs=normalize_hash_inputs,
            hash_exclude_args=hash_exclude_args,
            hash_include_args=hash_include_args,
            f_hash=f_hash,
        )

    def _initialize_context_lock(self, safety):
        """initialize context lock used for thread or process safety"""
        if safety == 'thread':
            self.lock = threading.RLock()
        elif safety == 'process':
            self.lock = multiprocessing.RLock()
        elif safety is None:
            # nullcontext in python3.7 and above
            # see https://stackoverflow.com/a/45187287
            if hasattr(contextlib, 'nullcontext'):
                self.lock = contextlib.nullcontext()
            else:
                self.lock = contextlib.suppress()
        else:
            raise Exception('safety must be \'thread\', \'process\', or None')

