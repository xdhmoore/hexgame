from hex.position import Position
from typing import Dict, List, Tuple


# TODO save state in numpy array?
class Board:
    NUM_PIECES_PER_TEAM = 11
    # TODO can I make this package private?
    # https://en.wikipedia.org/wiki/Hexagonal_Efficient_Coordinate_System
    # board: List[List[List[int]]]

    def __init__(self) -> None:
        # TODO might be interesting to implement this with a small graph db like cogdb
        # RESUME - make this a map from hex location to piece
        self.pieces = dict()
        self.edgeHead = None
        self.edgeTail = None
        self.step = 0

    def move(self, piece, pos):
        piece._move(self, pos)
        piece.pos = pos
        self.pieces[id(piece)] = piece
        self.step += 1

    def take_step(self):
        self.step += 1

    def is_occupied(self, pos: Position):
        # return len([filter(self.pieces.values if piece.pos.arc == pos.arc]) > 0
        # return any(piece for piece in self.pieces.values if piece.pos.arc == pos.arc)
        return (
            len(
                list(
                    filter(lambda piece: piece.pos.arc == pos.arc, self.pieces.values())
                )
            )
            > 0
        )

    # def get_edge_positions(self):
