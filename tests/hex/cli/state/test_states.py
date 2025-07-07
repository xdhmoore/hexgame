

import blessed
import pytest
from hex.board import Board
from hex.cli.screen_manager import ScreenManager
from hex.cli.state.abstract import AbstractState
from hex.cli.state.pick_piece_placement import PickPiecePlacementState
from hex.cli.state.pick_piece_type import PickPieceTypeState
from hex.cli.utils import new_keystroke
from hex.piece import Piece
from hex.piece_type import PieceType
from hex.player import Player
from hex.position import Position


class TestStates:
   # RESUME make this more readable, just feed in a list of keystrokes maybe grouped by turn 
   # or just make comments
   # write some more tests that involve board piece and move selection.

   def test_basic_arrows(self) -> None:
      term = blessed.Terminal()
      # TODO how to move this into shared function or ffixture?
      with term.fullscreen(), term.cbreak(), term.hidden_cursor():
         board = Board()
         mgr = ScreenManager(board, term)
         state: AbstractState = PickPieceTypeState(term, board)
         prev_move = board.last_move()
         assert prev_move is None
         assert mgr.get_piece_bank_selected() == (Player.Player1, PieceType.Ant)

         # TODO remove all the u'' stuff. it's only for backwards compatibility with python 2
         state, changed = state.on_key(new_keystroke(term, name=u'KEY_RIGHT'), mgr)
         assert changed
         assert board.curr_player == Player.Player1
         assert isinstance(state, PickPieceTypeState)
         prev_move = board.last_move()
         assert prev_move is None
         assert mgr.get_piece_bank_selected() == (Player.Player1, PieceType.Beetle)

         state, changed = state.on_key(new_keystroke(term, ucs=u'o'), mgr)
         assert not changed
         assert board.curr_player == Player.Player1
         assert isinstance(state, PickPieceTypeState)
         prev_move = board.last_move()
         assert prev_move is None
         assert mgr.get_piece_bank_selected() == (Player.Player1, PieceType.Beetle)

         state, changed = state.on_key(new_keystroke(term, ucs=u'd'), mgr)
         assert changed
         assert board.curr_player == Player.Player1
         assert isinstance(state, PickPieceTypeState)
         prev_move = board.last_move()
         assert prev_move is None
         assert mgr.get_piece_bank_selected() == (Player.Player1, PieceType.Beetle)


   def test_basic_wasd(self) -> None:
      term = blessed.Terminal()
      # TODO how to move this into shared function or ffixture?
      with term.fullscreen(), term.cbreak(), term.hidden_cursor():
         board = Board()
         mgr = ScreenManager(board, term)
         state: AbstractState = PickPieceTypeState(term, board)
         prev_move = board.last_move()
         assert prev_move is None
         assert mgr.get_piece_bank_selected() == (Player.Player1, PieceType.Ant)

         state, changed = state.on_key(new_keystroke(term, ucs=u'w'), mgr)
         assert changed
         assert board.curr_player == Player.Player1
         assert isinstance(state, PickPieceTypeState)
         prev_move = board.last_move()
         assert prev_move is None
         assert mgr.get_piece_bank_selected() == (Player.Player1, PieceType.Ant)

         state, changed = state.on_key(new_keystroke(term, ucs=u'o'), mgr)
         assert not changed
         assert board.curr_player == Player.Player1
         assert isinstance(state, PickPieceTypeState)
         prev_move = board.last_move()
         assert prev_move is None
         assert mgr.get_piece_bank_selected() == (Player.Player1, PieceType.Ant)

         state, changed = state.on_key(new_keystroke(term, ucs='d'), mgr)
         assert changed
         assert board.curr_player == Player.Player1
         assert isinstance(state, PickPieceTypeState)
         prev_move = board.last_move()
         assert prev_move is None
         assert mgr.get_piece_bank_selected() == (Player.Player1, PieceType.Ant)

   def test_first_move(self) -> None:
      term = blessed.Terminal()
      # TODO how to move this into shared function or ffixture?
      with term.fullscreen(), term.cbreak(), term.hidden_cursor():
          self.first_move(term)


# TODO make all this easier to read. parameterize the tests or just some functions to call
   def test_second_placement(self) -> None:
      term = blessed.Terminal()
      # TODO how to move this into shared function or ffixture?
      with term.fullscreen(), term.cbreak(), term.hidden_cursor():
         board, mgr = self.first_move(term)

         state, changed = mgr.on_key(new_keystroke(term, ucs=u'o'))
         assert not changed
         assert board.curr_player == Player.Player2
         assert isinstance(state, PickPieceTypeState)
         last_player: Player
         last_piece: Piece
         last_pos: Position
         last_player, last_piece, last_pos = board.last_move()
         assert last_player == Player.Player1
         assert last_piece.type == PieceType.Ant
         assert last_piece.pos == last_pos
         assert last_pos == Position(0, 0, 0)
         assert mgr.get_piece_bank_selected() == (Player.Player2, PieceType.Ant)

         state, changed = state.on_key(new_keystroke(term, name='KEY_ENTER'), mgr)
         assert changed
         assert board.curr_player == Player.Player1
         assert isinstance(state, PickPiecePlacementState)
         last_player: Player
         last_piece: Piece
         last_pos: Position
         last_player, last_piece, last_pos = board.last_move()
         assert last_player == Player.Player2
         assert last_piece.type == PieceType.Ant
         assert last_piece.pos == last_pos
         # TODO
         #assert last_pos == Position(0, 0, 0)
         assert mgr.get_piece_bank_selected() == (Player.Player1, PieceType.Ant)


   def first_move(self, term):
         board = Board()
         mgr = ScreenManager(board, term)
         state: AbstractState = PickPieceTypeState(term, board)
         prev_move = board.last_move()
         assert prev_move is None

         state, changed = state.on_key(new_keystroke(term, name='KEY_ENTER'), mgr)
         assert changed
         assert board.curr_player == Player.Player2
         assert isinstance(state, PickPieceTypeState)
         last_player: Player
         last_piece: Piece
         last_pos: Position
         last_player, last_piece, last_pos = board.last_move()

         assert last_player == Player.Player1
         assert last_piece.type == PieceType.Ant
         assert last_piece.pos == last_pos
         assert last_pos == Position(0, 0, 0)

         return board, mgr
