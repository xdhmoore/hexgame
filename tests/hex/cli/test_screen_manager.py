from typing import List
from unittest.mock import Mock

import pytest

from hex.board import Board
from hex.cli.cli_game import CliGame
from hex.cli.screen_cell import ScreenCell
from hex.cli.screen_manager import ScreenManager
from hex.cli.screen_position import ScreenPos
from hex.piece import Piece
from hex.position import Position


class TestScreenManager:

    @pytest.mark.parametrize(
        "bounds,center",
        [
            ((2, 4), (1, 2)),
            ((3, 5), (1, 2)),
        ],
    )
    def test_get_screen_center(self, bounds: tuple, center: tuple):
        term = Mock()
        term.height = bounds[0]
        term.width = bounds[1]
        board = Mock()
        board.pieces = []
        board.map.occupied_positions = lambda: []
        mgr = ScreenManager(board, term)
        actual_center = mgr.get_screen_center()
        assert actual_center == center
