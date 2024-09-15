from hex.cli.keys import Keys
from hex.cli.screen_cell import ScreenCell
from hex.cli.screen_position import ScreenPos
from hex.position import Position


class SelectorCell(ScreenCell):
    def __init__(self, pos: Position):
        self._pos = pos
        self.bold = True
        self.piece = None

    def move(self, key: int):
        # TODO may need to grab the piece of the dest place to be able to display it's name
        # Also may want to convert to hex coordinates? or maybe that's unneeded
        # a, r, c

        # TODO redo this with numpy
        # RESUME - redo the hex to screen mapping to be 90deg like michael said
        match key.code:
            case Keys.UP:
                new_pos = self.pos._top().axy
                # new_pos = (self.pos.a + 1 % 2, self.pos.r -1, self.pos.c)
            case Keys.DOWN:
                new_pos = self.pos._bottom().axy
                #new_pos = (self.pos.a + 1 % 2, self.pos.r+1, self.pos.c)
                # RESUME left and right don't work. How to calculate left/right in hex space
            case Keys.LEFT:
                if self.pos.a == 0:
                    new_pos = self.pos._top_left().axy
                else:
                    new_pos = self.pos._bottom_left().axy
                # new_pos = (self.pos.a, self.pos.r, self.pos.c - 1)
            case Keys.RIGHT:
                if self.pos.a == 0:
                    new_pos = self.pos._top_right().axy
                else:
                    new_pos = self.pos._bottom_right().axy
                # new_pos = (self.pos.a, self.pos.r, self.pos.c + 1)
            case default:
                new_pos = self.pos.axy

        # TODO does setting this mean I can end up with a mismatched self.piece?
        # Why have a property when I always use _pos?
        self._pos = Position(*new_pos)
