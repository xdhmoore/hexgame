from functools import reduce
import logging
from typing import List
from blessed import Terminal
from hex.board import Board
from hex.cli.keys import Keys
from hex.cli.screen_cell import ScreenCell
from hex.cli.screen_position import ScreenPos
from hex.cli.selector_cell import SelectorCell
from hex.cli.templates.template import Template
from hex.position import Position


class ScreenManager:
    def __init__(self, board: Board, term: Terminal):
        self.board = board
        self.term = term
        self.display_buff: List[List[str]] = []
        self.clear_display_buff()
        self.step = board.step
        self.selector = None
        self.dirty = True

    # TODO if needed
    # def on_resize

    def display(self) -> None:
        assert self.step <= self.board.step

        if self.step == self.board.step and not self.dirty:
            return

        self.step = self.board.step

        self.clear_display_buff()
        self.draw_pieces()
        self.draw_selector()
        self.flush_buffer()

    def get_cells_to_draw(self) -> List[ScreenCell]:
        cells = [ScreenCell(piece) for piece in self.board.pieces.values()] + [
            self.selector
        ]

    def draw_pieces(self) -> None:
        cells = [ScreenCell(piece) for piece in self.board.pieces.values()]
        self.draw_cells(cells)

    def draw_selector(self) -> None:
        if self.selector:
            self.draw_cells([self.selector])

    # TODO Make more typing mandatory -> Stuff
    # TODO add more docstrings
    def draw_cells(self, screen_cells) -> None:
        """Draws pieces and selector"""

        for screen_cell in screen_cells:
            screen_cell.draw(self.term, self.display_buff, self.get_viewport_offset())

    # TODO right now this functions as the viewport but at some point will want to make the viewport moveable
    def get_viewport_offset(self):
        return self.get_screen_center()

    def get_screen_center(self) -> tuple[int, int]:
        return ((self.term.height - 1) // 2, (self.term.width - 1) // 2)

    def init_selector(self) -> None:
        self.selector = SelectorCell(Position(0, 0, 0), self.board.get_piece_at_pos(Position(0,0,0)), self.board)

        self.dirty = True

    def move_selector(self, key: int) -> None:
        assert self.selector != None

        # TODO eventually may want to return T/F from this so it's not dirty if you run into an edge and can't move
        self.selector.move(key, self.board)
        self.dirty = True

    def clear_display_buff(self):
        display_buff_width = Board.NUM_PIECES_PER_TEAM * 4 * Template.WIDTH + 1
        display_buff_height = Board.NUM_PIECES_PER_TEAM * 4 * Template.HEIGHT + 1
        self.display_buff = [
            [None for i in range(display_buff_width)]
            for j in range(display_buff_height)
        ]

    def flush_buffer(self):
        out: str = self.term.clear + self.term.home
        c: str = None
        for y_idx, line in enumerate(self.display_buff):
            for x_idx, c in enumerate(line):
                if c:
                    # TODO there's probably a better way to do this by concatenating the c's in
                    # one line first...
                    # print(c + "d")
                    out += self.term.move_xy(x_idx, y_idx) + c  # '█'
        print(out, end="", flush=True)

    def get_draw_bounds(self, pieces: List[ScreenPos]):
        # TODO fix this to first get hex coord bounds, then convert
        (min_x, max_x, min_y, max_y) = self.get_bounds(pieces)
        # TODO
        return (
            min_x - ScreenCell.PAD_LEFT,
            max_x + ScreenCell.PAD_RIGHT,
            min_y - ScreenCell.PAD_TOP,
            max_y + ScreenCell.PAD_BOTTOM,
        )

    # TODO if needed make a datastructure for retrieving this sort of
    # info efficiently
    def get_bounds(self, pieces: List[ScreenPos]):

        # # TODO use iterables with all these maps in the correct way
        min_x = reduce(lambda x1, x2: min(x1, x2), map(lambda p: p.x, pieces))

        max_x = reduce(lambda x1, x2: max(x1, x2), map(lambda p: p.x, pieces))

        min_y = reduce(lambda y1, y2: min(y1, y2), map(lambda p: p.y, pieces))

        max_y = reduce(lambda y1, y2: max(y1, y2), map(lambda p: p.y, pieces))

        return (min_x, max_x, min_y, max_y)


r"""
 \__/  \__/
 /  \__/  \
 \__/  \__/
 /  \__/  \
"""
r"""
 \___/ 2 \___/
 / 2 \___/ 1 \
 \___/ 1 \___/
 /   \___/   \

"""
