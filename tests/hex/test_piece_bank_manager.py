

import blessed
from blessed import Terminal

from hex.board import Board
from hex.cli.piece_bank_manager import PieceBankManager
from hex.piece_bank import PieceBank
from hex.piece_type import PieceType
from hex.player import Player


class TestPieceBankManager:
    def test_build_str_other_turn(self):
        term = blessed.Terminal()
        board = Board()
        board.curr_player = Player.Player2
        with term.fullscreen(), term.cbreak(), term.hidden_cursor():
            mgr: PieceBankManager = PieceBankManager(
                board,
                Player.Player1,
                term
            )
            actual = mgr._build_str()
            expected = 'Player1 - a:3 b:2 g:3 l:1 m:1 p:1 q:1 s:4'
            assert expected == actual

    def test_draw_curr_player_turn(self):
        term = blessed.Terminal()
        board = Board()
        board.curr_player = Player.Player1
        with term.fullscreen(), term.cbreak(), term.hidden_cursor():
            mgr: PieceBankManager = PieceBankManager(
                Board(),
                Player.Player1,
                term
            )
            actual = mgr._build_str()
            expected = 'Player1 - [a:3] b:2 g:3 l:1 m:1 p:1 q:1 s:4'
            assert expected == actual


    def test_draw_selected_grasshopper(self):
        term = blessed.Terminal()
        with term.fullscreen(), term.cbreak(), term.hidden_cursor():
            mgr: PieceBankManager = PieceBankManager(
                Board(),
                Player.Player1,
                term,
            )
            mgr.select_next_piece()
            mgr.select_next_piece()
            actual = mgr._build_str()
            expected = 'Player1 - a:3 b:2 [g:3] l:1 m:1 p:1 q:1 s:4'
            assert expected == actual
            assert PieceType.Grasshopper == mgr.current_piece

    def test_select_prev_piece(self) -> None:
        term = blessed.Terminal()
        with term.fullscreen(), term.cbreak(), term.hidden_cursor():
            mgr: PieceBankManager = PieceBankManager(
                Board(),
                Player.Player1,
                term,
            )

            mgr.select_prev_piece()

            assert PieceType.Spider == mgr.current_piece