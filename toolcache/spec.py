import typing
from . import cachetypes


CommonCachetypeName = typing.Literal['disk', 'memory', 'null']
CachetypeSpec = typing.Union[CommonCachetypeName, 'cachetypes.BaseCache']

