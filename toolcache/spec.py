from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    from typing_extensions import Literal

    from . import cachetypes


    CommonCachetypeName = Literal['disk', 'memory', 'null']
    CachetypeSpec = typing.Union[CommonCachetypeName, 'cachetypes.BaseCache']
