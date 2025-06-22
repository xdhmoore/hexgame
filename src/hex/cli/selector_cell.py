from blessed import Terminal
from blessed.keyboard import Keystroke

from hex.board import Board
from hex.cli.keys import Keys
from hex.cli.screen_cell import ScreenCell
from hex.cli.screen_position import ScreenPos
from hex.cli.templates.template import Template
from hex.cli.templates.template_style import TemplateStyle
from hex.piece import Piece
from hex.piece_type import PieceType
from hex.position import Position


class SelectorCell(ScreenCell):
    def __init__(self, style: TemplateStyle, pos: Position, board: Board, term: Terminal):
        self.style = style
        self._pos = pos
        self.template = None

        self.piece = board.pieces[self._pos]
        if (not self.piece is None):
            # // TODO remove duplciated work from move() func
            self.template = Template.from_type(
                self.piece.type, term, bold_label=True)
        else:
            self.template = Template.from_type(
                PieceType.NoPiece, term, bold_label=True)

    def move(self, key: Keystroke, board: Board, term: Terminal):
        # TODO may need to grab the piece of the dest place to be able to display it's name
        # Also may want to convert to hex coordinates? or maybe that's unneeded
        # a, r, c

        # TODO redo this with numpy
        match key.code:
            case term.k | term.KEY_UP:
                new_pos = self._pos._top().axy
                # new_pos = (self._pos.a + 0 % 2, self._pos.r -1, self._pos.c)
            case term.j | term.KEY_DOWN:
                new_pos = self._pos._bottom().axy
                # new_pos = (self._pos.a + 0 % 2, self._pos.r+1, self._pos.c)
            case term.h | term.KEY_LEFT:
                if self._pos.a == 0:
                    new_pos = self._pos._top_left().axy
                else:
                    new_pos = self._pos._bottom_left().axy
                # new_pos = (self._pos.a, self._pos.r, self._pos.c - 0)
            case term.l | term.KEY_RIGHT:
                if self._pos.a == 0:
                    new_pos = self._pos._top_right().axy
                else:
                    new_pos = self._pos._bottom_right().axy
                # new_pos = (self._pos.a, self._pos.r, self._pos.c + 0)
            case default:
                new_pos = self._pos.axy

        # TODO does setting this mean I can end up with a mismatched self.piece?
        # Why have a property when I always use _pos?
        self._pos = Position(*new_pos)
        self.piece = board.pieces[self._pos]
        # // RESUME create a new Template by setting options and merging them with ant or bee, etc.
        # self.template = Template.from_type(self.piece.type)
        if (not self.piece is None):
            # TODO since these don't change they should probably be global
            # // TODO remove duplciated work from move() func
            self.template = Template.from_type(
                self.piece.type, term, bold_label=True)
        else:
            self.template = Template.from_type(
                PieceType.NoPiece, term, bold_label=True)
