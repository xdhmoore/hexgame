from blessed import Terminal

from hex.board import Board
from hex.cli.keys import Keys
from hex.cli.screen_cell import ScreenCell
from hex.cli.screen_position import ScreenPos
from hex.cli.templates.template import Template
from hex.piece import Piece
from hex.piece_type import PieceType
from hex.position import Position


class SelectorCell(ScreenCell):
    def __init__(self, pos: Position, piece: Piece, board: Board, term: Terminal):
        self._pos = pos
        self.activate = False
        self.template = None

        self.piece = board.get_piece_at_pos(self._pos)
        if (not self.piece is None):
            # // TODO remove duplciated work from move() func
            self.template = Template.from_type(
                self.piece.type, term, bold_label=True)
        else:
            self.template = Template.from_type(
                PieceType.NoPiece, term, bold_label=True)

    def move(self, key: int, board: Board, term: Terminal):
        # TODO may need to grab the piece of the dest place to be able to display it's name
        # Also may want to convert to hex coordinates? or maybe that's unneeded
        # a, r, c

        # TODO redo this with numpy
        match key.code:
            case Keys.UP:
                new_pos = self._pos._top().axy
                # new_pos = (self._pos.a + 0 % 2, self._pos.r -1, self._pos.c)
            case Keys.DOWN:
                new_pos = self._pos._bottom().axy
                # new_pos = (self._pos.a + 0 % 2, self._pos.r+1, self._pos.c)
            case Keys.LEFT:
                if self._pos.a == 0:
                    new_pos = self._pos._top_left().axy
                else:
                    new_pos = self._pos._bottom_left().axy
                # new_pos = (self._pos.a, self._pos.r, self._pos.c - 0)
            case Keys.RIGHT:
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
        self.piece = board.get_piece_at_pos(self._pos)
        # // RESUME create a new Template by setting options and merging them with ant or bee, etc.
        # self.template = Template.from_type(self.piece.type)
        if (not self.piece is None):
            # // TODO remove duplciated work from move() func
            self.template = Template.from_type(
                self.piece.type, term, bold_label=True)
        else:
            self.template = Template.from_type(
                PieceType.NoPiece, term, bold_label=True)
