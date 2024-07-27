import pytest
from hex.board import Board
from hex.cli.cli_game import CliGame
from hex.cli.screen_position import ScreenPos
from hex.piece import Piece
from hex.position import Position


class TestCliGame:
    def extract_positions(self, board: Board, cli_game: CliGame):
        return map(lambda piece: (piece, ScreenPos(piece.pos)), board.pieces.values())

    @pytest.mark.parametrize('placements,expected_bounds', [
        (((0, 0, 0), (1, -1, 0), (0, 0, 1)), (0, 4, -1, 1))
    ])
    def test_get_bounds(self, placements, expected_bounds):
        board = Board()
        cli_game = CliGame()

        for placement in placements:
            piece = Piece(None)
            board.move(piece, Position(*placement))
        pieces = list(self.extract_positions(board, cli_game))
        print("===========")
        print(list(map(lambda tup: tup[1], pieces)))
        print("===========")
        actual_bounds = cli_game.get_bounds(list(map(lambda tup: tup[1], pieces)))
        assert actual_bounds == expected_bounds


