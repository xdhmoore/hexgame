import logging
import re

from blessed import Terminal

from hex.cli.screen_position import ScreenPos
from hex.piece import Piece
from hex.position import Position

# TODO look into attr library or other more modern library for this?


class ScreenCell:

    def __init__(self, piece: Piece = None, pos: Position = None):

        if not piece is None and not pos is None:

            self.piece = piece
            self._pos = None
            assert ScreenPos(piece.pos) == pos

        elif not piece is None and pos is None:

            self.piece = piece
            self._pos = None

        elif not pos is None and piece is None:

            self._pos = pos
            self.piece = None

        else:
            assert False

        self.bold = False

    def draw(self, term: Terminal, buffer, viewport_offset: tuple[int, int] = (0, 0)):
        """
        Display a hexagonal tile on the screen, adjusting for the passed in viewport offset
        """

        screen_coords = (
            viewport_offset[0] + ScreenPos(self.pos).y,
            viewport_offset[1] + ScreenPos(self.pos).x,
        )

        logging.debug(f"draw() at {screen_coords}")
        for y_idx, line in enumerate(self.DRAWING):
            for x_idx, c in enumerate(line):
                # TODO pass in piece and display different symbol per kind and different color per player
                # TODO handle when piece is at edge of board?
                # TODO could change3 to handle empty strings or spaces better
                if c and c.strip():
                    y = y_idx - self.PAD_TOP + screen_coords[0]
                    x = x_idx - self.PAD_LEFT + screen_coords[1]

                    # TODO chagne to handle 3 cases:
                    # - when inside - draw
                    # - when just over - ignore
                    # - when way over - fail
                    OVERFLOW_ALLOWANCE_X = self.WIDTH * 2
                    OVERFLOW_ALLOWANCE_Y = self.HEIGHT * 2
                    if (
                        (y >= len(buffer) + OVERFLOW_ALLOWANCE_Y)
                        or (x >= len(buffer[y]) + OVERFLOW_ALLOWANCE_X)
                        or y <= -OVERFLOW_ALLOWANCE_Y
                        or x <= -OVERFLOW_ALLOWANCE_X
                    ):
                        # If it's not the center of the tile, just ignore if if it's over the edge of the board
                        # but only within an allowance
                        continue
                    if self.bold:
                        buffer[y][x] = term.bold_green(c)
                    else:
                        buffer[y][x] = c

    @property
    def pos(self):
        if not self.piece is None:
            return self.piece.pos
        elif not self._pos is None:
            return self._pos
        else:
            assert False

    @classmethod
    def init_class(cls):

        cls.CENTER_CHAR = "c"

        # TODO have multiple ascii drawings for different zoom settings?
        raw_drawing = r"""
             ___
            / c \
            \___/
        """

        cleaned_lines = [
            line for line in raw_drawing.splitlines() if line.strip() != ""
        ]
        # print(cleaned_lines)
        longest_line_length = 5
        num_lines = 3

        # shortest_indent = ...
        # TODO don't compile regex every time
        shortest_indent = min(
            map(
                lambda match: len(match.group()),
                [re.compile(r"^\s*").match(line) for line in cleaned_lines],
            )
        )
        # remove shortest indent from each line
        cls.DRAWING = [line[shortest_indent:] for line in cleaned_lines]
        # remove whitespace from any line on the right side
        # find coord of c
        for y_idx, line in enumerate(cls.DRAWING):
            c_x = line.find("c")
            if c_x != -1:
                cls.CENTER = (y_idx, c_x)
                break
        cls.PAD_TOP = cls.CENTER[0]
        cls.PAD_LEFT = cls.CENTER[1]
        cls.PAD_RIGHT = longest_line_length - cls.CENTER[1] - 1
        cls.PAD_BOTTOM = num_lines - cls.CENTER[0] - 1
        cls.WIDTH = cls.PAD_LEFT + 1 + cls.PAD_RIGHT
        cls.HEIGHT = cls.PAD_TOP + 1 + cls.PAD_BOTTOM


ScreenCell.init_class()
