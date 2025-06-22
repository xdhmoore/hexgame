from pprint import pprint
from typing import List
from unittest.mock import Mock

import blessed
import pytest

from hex.board import Board
from hex.cli.cli_game import CliGame
from hex.cli.screen_cell import ScreenCell
from hex.cli.screen_manager import ScreenManager
from hex.cli.screen_position import ScreenPos
from hex.cli.templates.template_style import TemplateStyle
from hex.cli.utils import new_buffer
from hex.piece import Piece
from hex.piece_type import PieceType
from hex.player import Player
from hex.position import Position

# TODO get code coverage working


class TestScreenCell:

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
        display_buff = new_buffer(20)
        term = blessed.Terminal()
        # TODO figure out dependency injection so I don't have to pass around term everywhere
        screen_cell = ScreenCell(
            term=term,
            style=TemplateStyle.Plain,
            piece=Piece(Position(*hex_pos), PieceType.Ant, Player.Player1)
        )
        screen_cell.draw(
            term=term, buffer=display_buff, player=Player.Player1, viewport_offset=(
                OFFSET, OFFSET)
        )
        print(display_buff)
        assert display_buff[screen_pos[0]][screen_pos[1]] == "a"
