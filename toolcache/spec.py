import typing
from typing_extensions import Literal

from . import cachetypes


CommonCachetypeName = Literal['disk', 'memory', 'null']
CachetypeSpec = typing.Union[CommonCachetypeName, 'cachetypes.BaseCache']

