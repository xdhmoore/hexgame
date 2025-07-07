

import logging

from blessed import Terminal
from blessed.keyboard import Keystroke

from hex.board import Board
from hex.piece import Piece
from hex.piece_bank import PieceBank, PieceBankInfo
from hex.player import Player


class PieceBankManager:

    def __init__(self, board: Board, player: Player, term: Terminal) -> None:
        self.board = board
        self.term: Terminal = term
        self.player = player
        self.selected_idx: int = 0

    @property
    def current_piece(self):
        return list(self.board.get_piece_bank(self.player).bank.keys())[self.selected_idx]

    def select_prev_piece(self):
        piece_bank = self.board.get_piece_bank(self.player)
        self.selected_idx = (self.selected_idx -
                             1) % len(piece_bank.bank.keys())
        # logging.debug(self.selected_idx)

    def select_next_piece(self):
        piece_bank = self.board.get_piece_bank(self.player)
        self.selected_idx = (self.selected_idx +
                             1) % len(piece_bank.bank.keys())

    # TODO assert buffer dimensions or use custom type?
    def draw(self, buffer: list[list]) -> None:
        bank_str = self._build_str()
        logging.debug(f"bank:{bank_str}")
        # TODO highlight line if it's a player's turn
        row_num = 0 if self.player == Player.Player1 else len(buffer) - 1
        for idx, c in enumerate(bank_str):
            buffer[row_num][idx] = c

    # TODO change delete to not yank

    def _build_str(self) -> str:
        # logging.debug("drawing piece bank for player " + self.player.name)
        output = self.player.name + " - "
        piece_bank = self.board.get_piece_bank(self.player)
        first = True

        # TODO when i use colors and special escapes does that screw up my buffer?
        # TODO do i even need a buffer?

        is_current_player = self.board.curr_player == self.player

        def build_bank_str_fragment(info: PieceBankInfo):

            # RESUME this is throwing list

            #  File "/workspaces/hexgame/src/hex/cli/piece_bank_manager.py", line 60, in _build_str
            #    return output + ' '.join(
            #                    ^^^^^^^^^
            #  File "/workspaces/hexgame/src/hex/cli/piece_bank_manager.py", line 53, in build_bank_str_fragment
            #    if is_current_player and info.type == list(piece_bank.bank.keys())[self.selected_idx]:
            #                                          ~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
            # IndexError: list index out of range

            # if is_current_player and info.type == list(PieceType)[self.selected_idx]:
            # TODO inefficient. check also other uses of bank.keys()
            if is_current_player and info.type == list(piece_bank.bank.keys())[self.selected_idx]:
                # TODO color this green
                return "[" + info.type.abbr + ':' + str(info.num) + "]"
            else:
                return info.type.abbr + ':' + str(info.num)

        # TODO order by original first, then expansions
        return output + ' '.join(
            map(
                build_bank_str_fragment,
                piece_bank.bank.values()
            )
        )

    # TODO change the selected piece type
    def move(self, key: Keystroke):
        piece_bank = self.board.get_piece_bank(self.player)
        # if key == self.term.KEY_LEFT or key == self.term.KEY_UP:

        # else if key == self.term.KEY_RIGHT or key == self.term.KEY_DOWN:

        # if piece_idx, piece in enumerate(piece_bank.bank.values):
        #     if piece

    def draw_to_terminal(self, term: Terminal, player: Player):
        pass  # output = self.draw(player)
        # TODO
