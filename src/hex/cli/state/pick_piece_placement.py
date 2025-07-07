import logging
from hex.cli.selector_cell import SelectorCell
from hex.cli.state.abstract import AbstractState, StateType
from hex.cli.templates.template_style import TemplateStyle
from hex.piece import Piece


class PickPiecePlacementState(AbstractState):

    def gs_type(self):
        return StateType.PICK_PIECE

    def __init__(self, term, board):
        self.term = term
        self.board = board

    def on_key(self, ks, mgr) -> tuple[AbstractState | None, bool]:
        actions_taken = False
        from hex.cli.state.pick_piece_type import PickPieceTypeState
        next_state = PickPieceTypeState(self.term, self.board)

        logging.debug("PICKPIECE")
        if (ks.code in [self.term.KEY_LEFT, self.term.KEY_RIGHT]):

            logging.debug("LEFT/RIGHT")
            current_piece_type = mgr.player_display_state_map[
                self.board.curr_player].piece_bank_mgr.current_piece
            # destinations = self.board.get_destinations( piece = Piece(Position(0, 0, 0), current_piece_type, self.board.get_curr_player())
            start_pos = mgr.selector._pos if mgr.selector else None

            start_positions = self.board.get_destinations(
                current_piece_type, start_pos)

            assert len(start_positions) > 0

            last_pos = (mgr.selector and mgr.selector._pos) or None
            if (last_pos in start_positions):
                last_pos_idx = start_positions.index(last_pos)
                if (ks.code == self.term.KEY_LEFT):
                    pos_idx = (last_pos_idx - 1) % len(start_positions)
                elif (ks.code == self.term.KEY_RIGHT):
                    pos_idx = (last_pos_idx + 1) % len(start_positions)
                else:
                    raise ValueError("Invalid arrow key")
            else:
                pos_idx = 0
            pos = start_positions[pos_idx]

            piece = Piece(pos, current_piece_type, self.board.curr_player)

            # if use_virtual_move:
            # TODO fail if not valid move
            # self.board.virtual_move(piece, pos)
            mgr.selector = SelectorCell(
                style=TemplateStyle.Selected,
                pos=pos,
                board=self.board,
                term=self.term,
            )
            # else:
            actions_taken = True
        elif (ks.code == self.term.ENTER or ks.code == self.term.KEY_ENTER):
            logging.debug("ENTER")
            next_state = PickPieceTypeState(self.term, self.board)
            current_piece_type = mgr.player_display_state_map[
                self.board.curr_player].piece_bank_mgr.current_piece
            last_pos = (mgr.selector and mgr.selector._pos) or None
            if last_pos is None:
                raise Exception("Invalid state. last_pos should be set")
            piece = Piece(last_pos, current_piece_type,
                          self.board.get_current_player())
            self.board.move(piece, last_pos, self.board.get_curr_player())
            actions_taken = True

        return super().on_key_shared(ks, mgr, next_state, actions_taken)
