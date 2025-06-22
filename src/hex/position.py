from dataclasses import dataclass
from typing import Any, ClassVar, List, Self


# TODO refactor to HexPosition or HEWhateverPosition
@dataclass(eq=True, unsafe_hash=True)
class Position:
    # Loosely inspired by https://en.wikipedia.org/wiki/Hexagonal_Efficient_Coordinate_System
    a: int  # array
    x: int  # row
    y: int  # column
# RESUME find all usages and refactor to new coordinates
# TODO should be class level?
    START: ClassVar[Self]

    def __init__(self, *args, **kwargs):
        if len(args) == 1:
            pos = args[0]
            self.a = pos.a
            self.x = pos.x
            self.y = pos.y

        elif len(args) == 3:
            self.a = args[0]
            self.x = args[1]
            self.y = args[2]

        else:
            raise ValueError(f"Invalid input to Position constructor: args:{
                             args}, kwargs:{kwargs}")

    # TODO move this stuff into the board class?
    # https://en.wikipedia.org/wiki/Hexagonal_Efficient_Coordinate_System#/media/File:HECS_Nearest_Neighbors.png

    def get_adjacent_positions(self) -> list[Self]:
        return [
            self._top(),
            self._top_right(),
            self._bottom_right(),
            self._bottom(),
            self._bottom_left(),
            self._top_left(),
        ]

    # "1 - a" has the effect of alternating between the two root arrays, the first coordinate which
    # can only be 0 or 1

    def _top_right(self) -> Self:
        if self.a == 0:
            return self.__class__(1 - self.a, self.x + 1, self.y)
        else:
            return self.__class__(1 - self.a, self.x + 1, self.y - 1)

    def _bottom_right(self) -> Self:
        if self.a == 0:
            return self.__class__(1 - self.a, self.x + 1, self.y + 1)
        else:
            return self.__class__(1 - self.a, self.x + 1, self.y)

    def _bottom(self) -> Self:
        return self.__class__(self.a, self.x, self.y + 1)

    def _bottom_left(self) -> Self:
        if self.a == 0:
            return self.__class__(1 - self.a, self.x - 1, self.y + 1)
        else:
            return self.__class__(1 - self.a, self.x - 1, self.y)

    def _top_left(self) -> Self:
        if (self.a == 0):
            return self.__class__(1 - self.a, self.x - 1, self.y)
        else:
            return self.__class__(1 - self.a, self.x - 1, self.y - 1)

    def _top(self) -> Self:
        return self.__class__(self.a, self.x, self.y - 1)

    def __str__(self):
        return f"({self.a},{self.x},{self.y})"

    def __repr__(self):
        return self.__str__()

    @property
    def axy(self):
        return (self.a, self.x, self.y)

    def _get_cmp_key(self):
        return (self.y, self.a, self.x)

    def __lt__(self, other: Self) -> bool:
        return self._get_cmp_key() < other._get_cmp_key()

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self._get_cmp_key() == other._get_cmp_key()

    # @property
    # def r(self):
    # should thsi be x or y?
        # return self.x


Position.START = Position(0, 0, 0)
