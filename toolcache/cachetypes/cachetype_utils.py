from __future__ import annotations

import typing

from .. import spec
from . import base_cache
from . import disk_cache
from . import memory_cache
from . import null_cache


def get_cache_class(
    cachetype: spec.CachetypeSpec,
) -> typing.Type[base_cache.BaseCache]:
    """return cachetype class given either cachetype name or cachetype class"""
    import inspect

    if isinstance(cachetype, str):
        if cachetype == 'disk':
            return disk_cache.DiskCache
        elif cachetype == 'memory':
            return memory_cache.MemoryCache
        elif cachetype == 'null':
            return null_cache.NullCache
    elif inspect.isclass(cachetype) and issubclass(
        cachetype, base_cache.BaseCache
    ):
        return cachetype

    raise Exception(
        'cachetype should be \'disk\', \'memory\''
        ', or a class that inherits from BaseCache'
        ', instead got: ' + str(cachetype)
    )

