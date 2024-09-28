import logging
import re
from typing import List

from blessed import Terminal

from hex.cli.screen_position import ScreenPos
from hex.cli.templates.template import Template
from hex.piece import Piece
from hex.position import Position

# TODO look into attr library or other more modern library for this?


class ScreenCell:

    def __init__(self, piece: Piece = None, pos: Position = None):

        if not piece is None and not pos is None:

            self.piece = piece
            self._pos = piece.pos
            assert ScreenPos(piece.pos) == pos

        elif not piece is None and pos is None:

            self.piece = piece
            self._pos = piece.pos

        elif not pos is None and piece is None:

            self._pos = pos
            self.piece = None

        else:
            assert False

        self.template = Template.from_type(piece.type)

    def draw(self, term: Terminal, buffer, viewport_offset: tuple[int, int] = (0, 0)):
        """
        Display a hexagonal tile on the screen, adjusting for the passed in viewport offset
        """

        screen_coords = (
            viewport_offset[0] + ScreenPos(self._pos).y,
            viewport_offset[1] + ScreenPos(self._pos).x,
        )

        logging.debug(f"draw() at {screen_coords}")
        # RESUME screen cell should use underlying piece's type template and override
        # parts of it
        self.template.draw(term, buffer, screen_coords, False)