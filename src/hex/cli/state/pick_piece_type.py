
import logging
from blessed import Terminal
from hex.board import Board
from hex.cli.selector_cell import SelectorCell
from hex.cli.state.abstract import AbstractState, StateType
from hex.cli.state.pick_piece_placement import PickPiecePlacementState
from hex.cli.templates.template_style import TemplateStyle
from hex.piece import Piece
from hex.position import Position


class PickPieceTypeState(AbstractState):

    def gs_type(self):
        return StateType.PICK_PIECE

    def __init__(self, term: Terminal, board: Board):
        self.term = term
        self.board = board

    # TODO add docstrings for return values
    def on_key(self, ks, mgr) -> tuple[AbstractState | None, bool]:
        next_state = self
        actions_taken = False
        logging.debug("PICKPIECETYPE")
        if (ks.code == self.term.KEY_LEFT):
            logging.debug("LEFT")
            mgr.player_display_state_map[self.board.curr_player].piece_bank_mgr.select_prev_piece(
            )
            actions_taken = True

        elif (ks.code == self.term.KEY_RIGHT):
            logging.debug("RIGHT")
            mgr.player_display_state_map[self.board.curr_player].piece_bank_mgr.select_next_piece(
            )
            actions_taken = True

        elif (ks.code == self.term.ENTER or ks.code == self.term.KEY_ENTER):
            logging.debug("ENTER")

            if (self.board.step > 0):
                next_state = PickPiecePlacementState(self.term, self.board)

            current_piece_type = mgr.player_display_state_map[
                self.board.curr_player].piece_bank_mgr.current_piece
            # TODO  these should come from the board's suggestion as the next available position
            piece = Piece(Position(0, 0, 0),
                          current_piece_type, self.board.get_curr_player())
            start_positions = self.board.get_destinations(piece.type, None)

            # if self.board.step > 0:
            #     # TODO fail if not valid move
            #     # self.board.virtual_move(piece, start_positions[0])
            #     mgr.selector = SelectorCell(
            #         style=TemplateStyle.Selected,
            #         pos=start_positions[0],
            #         board=self.board,
            #         term=self.term,
            #     )
            # else:
            self.board.move(
                    piece, start_positions[0], self.board.get_curr_player())
            actions_taken = True

        return super().on_key_shared(ks, mgr, next_state, actions_taken)

