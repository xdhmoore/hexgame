from pprint import pprint
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

# TODO get code coverage working


class TestScreenCell:

    def new_buffer(self, size: int) -> List[List[str]]:
        return [[None for i in range(size)] for j in range(size)]

    @pytest.mark.parametrize(
        "hex_pos,screen_pos",
        [
            # (1, 2),
            # (5, 5), # TODO more
            ((0, 0, 0), (9, 9))
        ],
    )
    def test_draw(self, hex_pos, screen_pos):
        BUFF_SIZE = 20
        OFFSET = BUFF_SIZE // 2 - 1
        display_buff = self.new_buffer(20)
        screen_cell = ScreenCell(pos=Position(*hex_pos))
        screen_cell.draw(
            term=Mock(), buffer=display_buff, viewport_offset=(OFFSET, OFFSET)
        )
        assert display_buff[screen_pos[0]][screen_pos[1]] == "c"

    def test_init(self):

        assert ScreenCell.DRAWING == [" ___", "/ c \\", "\\___/"]

        assert ScreenCell.CENTER == (1, 2)
        assert ScreenCell.PAD_TOP == 1
        assert ScreenCell.PAD_LEFT == 2
        assert ScreenCell.PAD_RIGHT == 2
        assert ScreenCell.PAD_BOTTOM == 1
        assert ScreenCell.WIDTH == 5
        assert ScreenCell.HEIGHT == 3
