"""toolcache makes it easy to create and configure caches in memory or on disk"""

from .cachetypes import (
    BaseCache,
    DiskCache,
    MemoryCache,
    get_cache_class,
)
from .cache_decorator import cache


__version__ = '0.5.0'

__all__ = (
    'BaseCache',
    'DiskCache',
    'MemoryCache',
    'get_cache_class',
    'cache',
)
