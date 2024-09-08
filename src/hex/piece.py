from typing import List

from hex.position import Position


class Piece:

    # TODO use kwargs so that pos is optional instead of requireing
    # None
    def __init__(self, pos: Position):
        self.pos = pos
        self.tr = None
        self.mr = None
        self.br = None
        self.bl = None
        self.ml = None
        self.tl = None

    # Use board.place or move instead
    def _move(self, board: Board, dest: Position) -> None:
        self.pos = dest
        self.tr = board.at(dest._top_right())
        self.mr = board.at(dest._mid_right())
        self.br = board.at(dest._bottom_right())
        self.bl = board.at(dest._bottom_left())
        self.ml = board.at(dest._mid_left())
        self.tl = board.at(dest._top_left())

        if not self.is_move_valid(board, dest):
            raise ValueError

    def is_move_valid(self, board: Board, dest: Position) -> bool:
        # TODO fix
        return True
        valid_moves = self.gen_valid_moves(board)
        return dest in self.gen_valid_moves(board)

    def gen_valid_moves(self, board: Board) -> List[Position]:
        return list(
            filter(lambda pos: not board.is_occupied(
                pos), self.gen_moves(board))
        )

    # TODO cache this
    # TODO override for different piece types
    # Generate moves without regard for whether the positions are occupied
    def gen_moves(self, board) -> List[Position]:
        # TODO fix
        return []
        # Get set/list of around board circumference, excluding unplayable points
        # if not self.pos:
        #     return board.get_edge_positions()
        # else:
        #     return self.pos.get_adjacent_positions()
