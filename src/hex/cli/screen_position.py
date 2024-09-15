from dataclasses import dataclass
from hex.position import Position


@dataclass
class ScreenPos:
    """
    ScreenPosition stores the terminal-space coordinates before adjusting for viewport. Probably the
    origin is the first tile played... TBD
    """

    x: int
    y: int

    def __init__(self, *args, **kwargs):
        # TODO fix this docstring
        """
        Init

        Usage
        ------------
        ScreenPos(position)
        ScreenPos(a, r, c)
        ScreenPos(y, x)
        """
        hex_pos = None

        if len(args) == 1 and len(kwargs.keys()) == 0:
            hex_pos: Position = args[0]

        if len(args) == 3 and len(kwargs.keys()) == 0:
            hex_pos = Position(*args[0:3])

        if hex_pos is not None:
            if (hex_pos.a == 0):
                self.x = 4 * hex_pos.x
                self.y = 2 * hex_pos.y
            else:
                self.x = 4 * hex_pos.x
                self.y = 2 * hex_pos.y - 1
            return

        if len(args) == 2 and len(kwargs.keys()) == 0:
            self.y = args[0]
            self.x = args[1]
            return

        raise ValueError("Invalid argument")

    @property
    def yx(self) -> tuple[2]:
        return (self.y, self.x)

    @property
    def xy(self) -> tuple[2]:
        return (self.x, self.y)
