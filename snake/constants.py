from enum import Enum
from typing import Type, Union

from plexapi.library import MovieSection, MusicSection, PhotoSection, ShowSection

SECTION_TYPE = Union[Type[MovieSection], Type[MusicSection], Type[PhotoSection], Type[ShowSection]]


class Operator(str, Enum):
    in_ = "in"
    gt = ">"
    lt = "<"
    gte = ">="
    lte = "<="
    eq = "="
