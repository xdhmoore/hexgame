
from dataclasses import dataclass
import logging
from typing import Any

from sortedcontainers import SortedDict
from hex.player import Player
from hex.position import Position


class Map:

    def __init__(self):
        self.mapmap = SortedDict()

    def get(self, pos: Position) -> "MapNode | None":
        return self.mapmap.get(pos)
    
    def get_piece(self, a, x, y): #-> Piece | None:
        # TODO more succinct verison of this
        node = self.get(Position(a, x, y))
        if (node is None):
            return None
        else:
            return node.piece
    
    def place(self, piece, pos:Position, player: Player):
        piece.pos = pos
        self.mapmap[piece.pos] = MapNode(self, piece);
    
    def occupied_positions(self) -> list[Position]:
        return [pos for pos in self.mapmap.keys()]

    def get_playable_edges(self):
        occupied = [
            pos for pos, node in self.mapmap.items()
        ]
        edges = []
        for o in occupied:
            edges += o.get_adjacent_positions()

        # TODO filter out
        return edges
    
    def occupied(self, pos:Position):
        return self.mapmap.get(pos) is not None

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

