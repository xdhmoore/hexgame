import logging
import re
from typing import List

from blessed import Terminal

from hex.cli.screen_position import ScreenPos
from hex.cli.templates.template import Template
from hex.cli.templates.template_style import TemplateStyle
from hex.piece import Piece
from hex.player import Player
from hex.position import Position

# TODO look into attr library or other more modern library for this?


class ScreenCell:

    def __init__(self, term: Terminal, style: TemplateStyle, piece: Piece, pos: Position | None = None):

        # print("-----------------")
        # print(piece)
        # print("---")
        # print(pos)

        self.style = style
        self.piece: Piece | None = None

        # piece, pos
        if not piece is None and not pos is None:

            self.piece = piece
            self._pos: Position = piece.pos
            assert ScreenPos(piece.pos) == pos

        # piece, _
        elif not piece is None and pos is None:

            self.piece = piece
            self._pos = piece.pos

        # _, pos
        # elif not pos is None and piece is None:

            # self._pos = pos
            # self.piece = None

        # _, pos, or _, _
        else:
            assert False

        self.template = Template.from_type(self.piece.type, term, )

    def draw(self, term: Terminal, buffer, player: Player, viewport_offset: tuple[int, int] = (0, 0)):
        """
        Display a hexagonal tile on the screen, adjusting for the passed in viewport offset
        """


        screen_coords = (
            viewport_offset[0] + ScreenPos(self._pos).y,
            viewport_offset[1] + ScreenPos(self._pos).x,
        )

        #(f"draw() at {screen_coords}")
        # RESUME - all draw's should send player
        # also, start back on cli game logic
        self.template.draw(term, buffer, screen_coords, {
                           'hex_pos': self._pos}, self.style, player)
