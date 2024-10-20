from typing import Dict, List, Tuple

from hex.piece import Piece
from hex.position import Position


# TODO save state in numpy array?
class Board:
    NUM_PIECES_PER_TEAM = 11
    # TODO can I make this package private?
    # https://en.wikipedia.org/wiki/Hexagonal_Efficient_Coordinate_System
    # board: List[List[List[int]]]

    def __init__(self) -> None:
        # TODO might be interesting to implement this with a small graph db like cogdb
        # TODO - make this a map from hex location to piece
        self.pieces = dict()
        self.pieces_by_pos: Dict[Position, Piece] = dict()
        # self.placements = dict()
        self.edgeHead = None
        self.edgeTail = None
        self.step = 0

    def get_piece_at_pos(self, pos: Position):
        return self.pieces_by_pos.get(pos)

    def move(self, piece: Piece, pos: Position) -> None:
        self.pieces_by_pos[piece.pos] = None
        piece._move(pos)
        self.pieces_by_pos[piece.pos] = piece
        self.pieces[id(piece)] = piece
        # TODO map to id instead to save space?
        # //self.placements[piece.pos] = piece
        self.step += 1

    def take_step(self):
        self.step += 1

    # def at(self, pos:Position) -> Position:
    #     return self.placements[pos]

    def is_occupied(self, pos: Position):
        # return len([filter(self.pieces.values if piece.pos.arc == pos.arc]) > 0
        # return any(piece for piece in self.pieces.values if piece.pos.arc == pos.arc)
        return (
            len(
                list(
                    filter(lambda piece: piece.pos.axy ==
                           pos.axy, self.pieces.values())
                )
            )
            > 0
        )

    # def get_edge_positions(self):
