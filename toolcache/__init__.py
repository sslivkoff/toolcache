"""functions for managing python caches"""

from .cachetypes import (
    BaseCache,
    DiskCache,
    MemoryCache,
    get_cache_class,
)
from .cache_decorator import cache

