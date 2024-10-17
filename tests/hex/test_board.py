from hex.board import Board
from hex.piece import Piece
from hex.piece_type import PieceType
from hex.position import Position


class TestBoard:
    def test_place(self):
        board = Board()
        piece = Piece(None, PieceType.Ant)
        assert not board.is_occupied(Position(0, 0, 1))
        board.move(piece, Position(0, 0, 1))
        assert board.is_occupied(Position(0, 0, 1))
