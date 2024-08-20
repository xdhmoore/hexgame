from typing import List
from unittest.mock import Mock
from hex.cli.screen_cell import ScreenCell
from hex.cli.screen_manager import ScreenManager
import pytest
from hex.board import Board
from hex.cli.cli_game import CliGame
from hex.cli.screen_position import ScreenPos
from hex.piece import Piece
from hex.position import Position


class TestScreenManager:

    @pytest.mark.parametrize('bounds,center', [
        ((2, 4), (0, 1)),
        ((3, 5), (1, 2)),
    ])
    def test_get_screen_center(self, bounds: tuple, center: tuple):
        term = Mock()
        term.height = bounds[0]
        term.width = bounds[1]
        mgr = ScreenManager(Mock(), term)
        actual_center = mgr.get_screen_center()
        assert actual_center == center

    # TODO fix
    # @pytest.mark.parametrize('term_bounds,relative_center,expected_center', [
    #     ((20, 20), (0, 0), (9, 9)),
    #     #((20, 20), (1, 1), ())
    # ])
    # def test_draw_at_terminal_center(self, term_bounds, relative_center, expected_center):
    #     term = Mock()
    #     term.height = term_bounds[0]
    #     term.width = term_bounds[1]
    #     screen_cell = ScreenCell(ScreenPos(*relative_center))
    #     buffer = self.new_buffer(20)
    #     screen_cell.draw(term, buffer, (term))
    #     # mgr = ScreenManager(Mock(), term)
    #     # mgr.display_space(ScreenPos(*relative_center))
    #     assert [expected_center[0]][expected_center[1]] == 'c'