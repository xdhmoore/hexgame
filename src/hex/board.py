from collections import OrderedDict
from dataclasses import dataclass
from functools import reduce
from typing import Callable, Dict, List, Tuple

from sortedcontainers import SortedDict

from hex.piece import Piece
from hex.piece_bank import PieceBank
from hex.player import Player
from hex.position import Position


@dataclass
class PlayerState:
    piece_bank: PieceBank

# TODO save state in numpy array?


class Board:
    # TODO use bank sum
    NUM_PIECES_PER_TEAM = 11
    # TODO can I make this package private?
    # https://en.wikipedia.org/wiki/Hexagonal_Efficient_Coordinate_System
    # board: List[List[List[int]]]

    def __init__(self) -> None:
        # TODO might be interesting to implement this with a small graph db like cogdb
        # TODO - make this a map from hex location to piece
        self.pieces  = SortedDict()
        self.virtual_pieces = dict()
        # self.placements = dict()
        self.edgeHead = None
        self.edgeTail = None
        self.step = 0
        self.player_state_map = dict()
        self.player_state_map[Player.Player1] = PlayerState(PieceBank())
        self.player_state_map[Player.Player2] = PlayerState(PieceBank())
        self.curr_player = Player.Player1

    def get_piece_bank(self, player) -> PieceBank:
        return self.player_state_map[player].piece_bank

    def get_curr_player(self):
        return self.curr_player

    def get_empty_pos(self) -> Position:
        edges = self.get_board_edges()
        if len(edges) < 1:
            # TODO msg
            raise RuntimeError()
        # TODO is this good enough? Return random edge node? Maybe return closest edge node to center?
        return edges[0]

    def get_board_edges(self) -> list[Position]:
        return [
            pos
            for piece in self.pieces.values()
            for pos in piece.pos.get_adjacent_positions()
            if not self.is_occupied(pos)
            # handle "cannot slide into" issue
            if len(piece.get_adjacent_pieces()) < 5
        ]

    def get_recommended_pos(self) -> Position:
        return self.get_empty_pos()

    def filter_blocked_piees(self, pieces) -> list[Piece]:
        return [p for p in pieces if self._piece_reachable(p)]

    def _piece_reachable(self, p: Piece):
        pass

    '''
            # Calculate square wrapping pieces (in hex space?)
            # Pick the hex location just outside the square that is closest
            # to the target piece
            # run A* to find a path from the piece to the edge. Do not allow path to cross over
            # too tight of spaces
            # if A* finds the target edge OR a past-reachable space, it is reachable. if it does not, it is not.
            # Save all the reachable spaces for next target space

            # There should be a way to only search a path around the edge of the
            # pieces, instead of trying to do a search for the wrapping square edge every time

            # TODO I think i need this in cartesian space, not hex space...'
    '''

    '''
        OR
        Calculate square wrapping cluster. Pick a square touching edge square. If there are
            multiple pieces touching this edge pick the most counter-clockwise one.
            This square is guaranteed to be reachable. This square will have
            at least 1 outer, open edge.
        
        Clockwise from that edge, find the first occupied adjacent space.
        Counter-clockwise from that space, is that piece reachable respecting
            the slide rule? If so it is reachable.

        Look at this next piece. Starting at the edge connecting it to the previous piece, go
        counter clockwise through the edges until you find an open adjacent space.

        OR
        Goal is to define one or more clusters of adjacent pieces. Start with an unoccupied edge space.
        This is the outside cluster. One by one expand the outside cluster based on if spaces are
        adjacent via more than 1 edge. If they are adjacent by 1 edge only, this is an unreachable cluster.
        Expansion of clusters could be done in parallel or probably partially cached.
    '''

    # Find boundaries of board 1 step past min/max pieces. Let this be the played square
    # Define set of all spaces in square
    # Place all occupied spaces in occupied set
    # Circle the board until a piece with no adjacent occupied space is found. This is the free space set.
    # Iterate over the edges of the free space set. If a neighbor is adjacent to an occupied space, put it in the adjacent free set, unless it is a neighbor to the free set only by one edge. Then it goes into a new captive cluster. There may be more than one of these.

    # It may be possible to maintain a data structure of this cluster info that updates as the game is played.

    def calc_board_boundaries(self):
        # RESUME
        # TODO will this work with hex coords?
        # TODO take advantage of pieces sorteddict ordering to get max/min of at least y coord
        return reduce(lambda a, b: min(a.pos.r, b.pos.r), self.pieces)
    

    def clear_virtual_pieces(self) -> None:
        self.virtual_pieces = dict()

    def virtual_move(self, piece: Piece, pos: Position) -> bool:
        # self.pieces_by_pos[piece.pos] = None
        if not piece._move(self.pieces, pos):
            return False

        self.virtual_pieces[id(piece)] = piece
        # TODO map to id instead to save space?
        # //self.placements[piece.pos] = piece
        return True

    # TODO change callers to handle when this returns false
    def move(self, piece: Piece, pos: Position) -> bool:
        # self.pieces_by_pos[piece.pos] = None
        if not piece._move(self.pieces, pos):
            return False

        self.curr_player = self.curr_player.next()
        # TODO map to id instead to save space?
        # //self.placements[piece.pos] = piece
        self.step += 1

        return True

    def take_step(self):
        self.step += 1

    # def at(self, pos:Position) -> Position:
    #     return self.placements[pos]

    def is_occupied(self, pos: Position):
        # return len([filter(self.pieces.values if piece.pos.arc == pos.arc]) > 0
        # return any(piece for piece in self.pieces.values if piece.pos.arc == pos.arc)
        matches_position: Callable[[Piece],
                                   bool] = lambda piece: piece.pos.axy == pos.axy
        # TODO this shouldn't be necessary with new SortedDict
        return (
            len(
                list(
                    filter(matches_position, self.pieces.values())
                )
            )
            > 0
        )

    # def get_edge_positions(self):
