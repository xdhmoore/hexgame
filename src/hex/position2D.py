from dataclasses import dataclass
from typing import Any, List, Self


# TODO refactor to HexPosition or HEWhateverPosition
@dataclass
class Position:
    # https://en.wikipedia.org/wiki/Hexagonal_Efficient_Coordinate_System
    y: int  # row
    x: int  # array
    def __init__(self, *args, **kwargs):
        if len(args) == 1:
            pos = args[0]
            self.y = pos.y
            self.x = pos.x

        elif len(args) == 2:
            self.y = args[0]
            self.x = args[1]
        
        else:
            raise ValueError(f"Invalid input to Position constructor: args:{args}, kwargs:{kwargs}")
        

    # TODO move this stuff into the board class?
    # https://en.wikipedia.org/wiki/Hexagonal_Efficient_Coordinate_System#/media/File:HECS_Nearest_Neighbors.png
    def get_adjacent_positions(self) -> List[Self]:
        return [
            self._top_right(),
            self._mid_right(),
            self._bottom_right(),
            self._bottom_left(),
            self._mid_left(),
            self._top_left(),
        ]

    # "1 - a" has the effect of alternating between the two root arrays, the first coordinate which
    # can only be 0 or 1

    def _top_right(self) -> Self:
        return Position(1 - self.a, self.r - (1 - self.a), self.c + self.a)

    def _mid_right(self) -> Self:
        return Position(self.a, self.r, self.c + 1)

    def _bottom_right(self) -> Self:
        return Position(1 - self.a, self.r + self.a, self.c + self.a)

    def _bottom_left(self) -> Self:
        return Position(1 - self.a, self.r + self.a, self.c - (1 - self.a))

    def _mid_left(self) -> Self:
        return Position(self.a, self.r, self.c - 1)

    def _top_left(self) -> Self:
        return Position(1 - self.a, self.r - (1 - self.a), self.c - (1 - self.a))

    def __str__(self):
        return f"({self.a},{self.r},{self.c})"

    def __repr__(self):
        return self.__str__()

    @property
    def arc(self):
        return (self.a, self.r, self.c)


Position.START = Position(0, 0, 0)
