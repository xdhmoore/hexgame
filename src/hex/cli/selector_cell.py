from hex.cli.keys import Keys
from hex.cli.screen_cell import ScreenCell
from hex.cli.screen_position import ScreenPos


class SelectorCell(ScreenCell):
    def __init__(self, screen_pos: ScreenPos = None):
        self.screen_pos = screen_pos
        self.bold = True

    def move(self, key: int):
        # TODO may need to grab the piece of the dest place to be able to display it's name
        # Also may want to convert to hex coordinates? or maybe that's unneeded
        delta = ()

        # RESUME
        match key:
            case Keys.UP:
                delta = (-1, 0)
            case Keys.DOWN:
                delta = (1, 0)
            case Keys.LEFT:
                delta = (0, -1)
            case Keys.RIGHT:
                delta = (0, 1)
