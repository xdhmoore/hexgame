

from enum import Enum
from typing import Self


class TypeEnum(Enum):
    TypeA = 1
    TypeB = 2
    TypeC = 3


class Scratch:

    def __init__(self, t: TypeEnum, color: str, label: str) -> None:
        # logic based on type enum
        pass

    @classmethod
    def create(cls, t: TypeEnum) -> Self:
       # TODO reproduce template.py static error
        return cls(t, 'red', 'hello')
