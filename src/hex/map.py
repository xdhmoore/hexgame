
from dataclasses import dataclass
from typing import Any
from hex.player import Player
from hex.position import Position


class Map:

    def __init__(self):
        self.mapmap: dict[tuple[int, int, int], MapNode] = dict()

    # RESUME
    def get(self, a, x, y) -> "MapNode | None":
        return self.mapmap.get((a, x, y))
    
    def get_piece(self, a, x, y): #-> Piece | None:
        # TODO more succinct verison of this
        node = self.get(a, x, y)
        if (node is None):
            return None
        else:
            return node.piece
    
    def place(self, piece, pos:Position, player: Player):
        piece.pos = pos
        self.mapmap[piece.pos.axy] = MapNode(self, piece);
    
    def occupied_positions(self) -> list[Position]:
        return [Position(a, x, y) for a, x, y in self.mapmap.keys()]

    def get_playable_edges(self):
        edges = [
            Position(a, x, y)
            for (a, x, y), node in self.mapmap.items()
            if node is not None
        ]
        # TODO filter out
        return edges
    
    def occupied(self, pos:Position):
        return self.mapmap.get(pos.axy) is not None

@dataclass
class MapNode:
    map: Map
    piece: Any

    def __init__(self, map: Map, piece):
        self.map = map
        self.piece = piece

    def find_board_edge(self, path:"list[MapNode]"):
        # get neighbors. sort them by highest x to lowest, then highest to lowest y
        # for each neighbor
            # add neighbor to path
            # if location of neighbor is X
        neighbors = [
        ]

