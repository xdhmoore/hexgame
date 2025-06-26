
from __future__ import annotations

import abc
import logging
import math
import time

# TODOccleanup
from abc import ABC, ABCMeta, abstractmethod
from dataclasses import dataclass
from enum import Enum, StrEnum
from functools import reduce
from operator import add
from threading import Lock
from typing import List, Self, Sequence, Tuple

from blessed import Terminal
from blessed.keyboard import Keystroke

from hex.board import Board
from hex.cli.keys import Keys
from hex.cli.piece_bank_manager import PieceBankManager
from hex.cli.screen_cell import ScreenCell
from hex.cli.screen_position import ScreenPos
from hex.cli.selector_cell import SelectorCell
from hex.cli.templates.template import Template
from hex.cli.templates.template_style import TemplateStyle
from hex.piece import Piece
from hex.piece_type import PieceType
from hex.player import Player
from hex.position import Position


@dataclass
class PlayerDisplayState:
    piece_bank_mgr: PieceBankManager


class GameStateType(StrEnum):
    PICK_PIECE = ("PICK_PIECE")
    PLACE_PIECE = ("PLACE_PIECE")

    def __init__(self, type):
        self.type = type


class AbstractGameState(ABC):
    _instance = None

    # Singleton
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @abstractmethod
    def on_key(self, ks, mgr) -> tuple[Self | None, bool]:
        pass

    @abstractmethod
    def gs_type(self) -> GameStateType:
        pass

    def on_key_shared(self, ks: Keystroke, mgr, next_state, actions_taken) -> tuple[Self | None, bool]:

        if ks == 'w' or ks == 'W':
            mgr.view_offset = (
                mgr.view_offset[0] - 1,
                mgr.view_offset[1]
            )
            actions_taken = True

        if ks == 's' or ks == 'W':
            mgr.view_offset = (
                mgr.view_offset[0] + 1,
                mgr.view_offset[1]
            )
            actions_taken = True

        if ks == 'a' or ks == 'A':
            mgr.view_offset = (
                mgr.view_offset[0],
                mgr.view_offset[1] - 1,
            )
            actions_taken = True

        if ks == 'd' or ks == 'D':
            mgr.view_offset = (
                mgr.view_offset[0],
                mgr.view_offset[1] + 1,
            )
            actions_taken = True

        return (next_state, actions_taken)

# TODO put all these handler classes in their own file


class PlacePieceGameState(AbstractGameState):

    def gs_type(self):
        return GameStateType.PICK_PIECE

    def __init__(self, term, board):
        self.term = term
        self.board = board

    def on_key(self, ks, mgr) -> tuple[AbstractGameState | None, bool]:
        next_state = None
        actions_taken = False
        if mgr.selector == None:
            # TODO words in errors
            #raise RuntimeError()
            pass
        elif mgr.selector.piece == None:
            # TODO when you're placing but the selector isn't over a real place

            raise RuntimeError()
        else:
            if (ks.code == self.term.ENTER or ks.code == self.term.KEY_ENTER):
                self.board.clear_virtual_pieces()
                self.board.move(mgr.selector.piece,
                                pos=mgr.selector._pos)
                next_state = PickPieceGameState(self.term, self.board)
            actions_taken = True

        return super().on_key_shared(ks, mgr, next_state, actions_taken)


class PickPieceGameState(AbstractGameState):

    def gs_type(self):
        return GameStateType.PICK_PIECE

    def __init__(self, term: Terminal, board: Board):
        self.term = term
        self.board = board

    def on_key(self, ks, mgr) -> tuple[AbstractGameState | None, bool]:
        next_state = None
        actions_taken = False
        if (ks.code == self.term.KEY_LEFT):
            # logging.debug('in branch')
            mgr.player_display_state_map[self.board.curr_player].piece_bank_mgr.select_prev_piece(
            )
            actions_taken = True

        elif (ks.code == self.term.KEY_RIGHT):
            mgr.player_display_state_map[self.board.curr_player].piece_bank_mgr.select_next_piece(
            )
            actions_taken = True

        elif (ks.code == self.term.ENTER or ks.code == self.term.KEY_ENTER):

            if (self.board.step > 0):
                next_state = PlacePieceGameState(self.term, self.board)

            current_piece_type = mgr.player_display_state_map[
                self.board.curr_player].piece_bank_mgr.current_piece
            # TODO  these should come from the board's suggestion as the next available position
            piece = Piece(Position(0, 0, 0),
                          current_piece_type, self.board.get_curr_player())
            start_positions, use_virtual_move = self.board.get_destinations(piece.type, None)

            if use_virtual_move:
                # TODO fail if not valid move
                self.board.virtual_move(piece, start_positions[0])
                mgr.selector = SelectorCell(
                    style=TemplateStyle.Selected,
                    pos=start_positions[0],
                    board=self.board,
                    term=self.term,
                )
            else:
                self.board.move(piece, start_positions[0], self.board.get_curr_player())
            actions_taken = True

        return super().on_key_shared(ks, mgr, next_state, actions_taken)


class ScreenManager:
    def __init__(self, board: Board, term: Terminal, debug: bool = False, slow_display=True):
        self.debug = debug
        self.slow_display = slow_display
        self.board = board
        self.term = term
        self.display_buff: list[list[str | None]] = []
        self.clear_display_buff()
        self.step = board.step
        self.selector: None | SelectorCell = None
        # RESUME - make a demo that displays screen grid w/ arc coordinates or xy coordinates
        # will help with doing algorithms on arc coordinates
        self.dirty = True
        self.state: AbstractGameState = PickPieceGameState(term, board)
        self.selected_type: None | PieceType = None

        self.view_offset: tuple[int, int] = (0, 0)

        # logging.debug(self.board.map.occupied_positions())
        if len(self.board.map.occupied_positions()) > 0:

            min_x = math.inf
            max_x = - math.inf
            min_y = math.inf
            max_y = - math.inf

            for pos in [ScreenPos(p) for p in self.board.map.occupied_positions()]:
                min_x = min(min_x, pos.x)
                min_y = min(min_y, pos.y)
                max_x = max(max_x, pos.x)
                max_y = max(max_y, pos.y)

            self.view_offset: tuple[int, int] = (
                - math.floor((min_y + max_y) / 2),
                - math.floor((min_x + max_x) / 2),
            )

        self.player_display_state_map: dict[Player,
                                            PlayerDisplayState] = dict()
        self.player_display_state_map[Player.Player1] = PlayerDisplayState(
            PieceBankManager(
                board,
                Player.Player1,
                self.term,
            )
        )
        self.player_display_state_map[Player.Player2] = PlayerDisplayState(
            PieceBankManager(
                board,
                Player.Player2,
                self.term,
            )
        )

    @property
    def cells(self):
        return [ScreenCell(self.term, (TemplateStyle.Debug if self.debug else TemplateStyle.Plain),  node.piece)  for node in self.board.map.mapmap.values()]

    # TODO hwo to do javadocs for methods, cclasses, etc
    # returns whether any action was taken that might need a redraw
    def onkey(self, key: Keystroke):
        actions_taken = False
        # logging.debug(self.state)
        next_state, actions_taken = self.state.on_key(key, self)
        if (next_state):
            self.state = next_state

        return actions_taken
    # TODO if needed
    # def on_resize

    def display(self) -> None:
        assert self.step <= self.board.step

        if self.step == self.board.step and not self.dirty:
            return

        self.step = self.board.step

        self.clear_display_buff()
        self.draw_pieces()
        self.draw_selector()
        self.draw_piece_banks()
        self.flush_buffer()

    # def get_cells_to_draw(self) -> list[ScreenCell | SelectorCell | None]:
    #     return [ScreenCell(piece, self.term) for piece in self.board.   pieces.values()] + [
    #         self.selector
    #     ]

    def draw_piece_banks(self) -> None:
        # logging.debug("drawing piece banks")
        # str_piece_bank = self.piece_bank_mgr1.draw(Player.Player1, PieceType
        self.player_display_state_map[Player.Player1].piece_bank_mgr.draw(
            self.display_buff)
        self.player_display_state_map[Player.Player2].piece_bank_mgr.draw(
            self.display_buff)

    def draw_pieces(self) -> None:
        # logging.debug("drawing pieces")
        self.draw_cells(self.cells)

    def draw_selector(self) -> None:
        if self.selector:
            # logging.debug("drawing selector")
            self.draw_cells([self.selector])

    # TODO Make more typing mandatory -> Stuff
    def draw_cells(self, screen_cells) -> None:
        """Draws pieces and selector"""

        # logging.debug(f"mgr viewport_offset:{self.get_viewport_offset()}")

        for screen_cell in reversed(screen_cells):
            if self.slow_display:
                time.sleep(0.2)
            # logging.debug(f"viewport_offset:${self.get_viewport_offset()}")
            screen_cell.draw(term=self.term,
                             buffer=self.display_buff,
                             player=Player.Player1,  # TODO update when turns implemented
                             viewport_offset=self.get_viewport_offset())
            if self.slow_display:
                self.flush_buffer()

    # TODO right now this functions as the viewport but at some point will want to make the viewport moveable
    def get_viewport_offset(self) -> tuple[int, int]:
        screen_center = self.get_screen_center()
        # logging.debug(f"screen center: ${screen_center}")
        # logging.debug(f"view offset: ${self.view_offset}")

        return (
            screen_center[0] + self.view_offset[0],
            screen_center[1] + self.view_offset[1]
        )

    # TODO change this to offset within player areas
    def get_screen_center(self) -> tuple[int, int]:
        # logging.debug(f"height:${self.term.height}, width:${self.term.width}")
        return ((self.term.height) // 2, (self.term.width) // 2)

    def init_selector(self) -> None:
        self.selector = SelectorCell(
            TemplateStyle.Hover, Position(0, 0, 0), self.board, self.term)
        self.dirty = True

    def move_selector(self, key: Keystroke) -> None:
        assert self.selector != None

        # TODO eventually may want to return T/F from this so it's not dirty if you run into an edge and can't move
        self.selector.move(key, self.board, self.term)
        self.dirty = True

    def move_piece_selector(self, key: Keystroke) -> None:
        curr_player = self.board.get_curr_player()
        display_state = self.player_display_state_map[curr_player]
        piece_bank_mgr = display_state.piece_bank_mgr
        piece_bank_mgr.move(key)

    def clear_display_buff(self):
        self.display_buff = self.build_display_buff()

    # TODO split this off into separate class for building buffer

    # TODO - is this buffer really necessary?
    def build_display_buff(self):
        buffer: list[list[str | None]] = [
            [None for i in range(self.term.width)]
            for j in range(self.term.height)
        ]

        return buffer

    def flush_buffer(self):
        # logging.debug("flushing buffer")
        out: str = self.term.clear + self.term.home
        c: str | None = None
        for y_idx, line in enumerate(self.display_buff):
            for x_idx, c in enumerate(line):
                if c:
                    # TODO there's probably a better way to do this by concatenating the c's in
                    # one line first...
                    # print(c + "d")
                    # logging.debug(f"plotting {c} at {x_idx},{y_idx})")
                    out += self.term.move_xy(x_idx, y_idx) + c  # '█'
        print(out, end="", flush=True)

    # def get_draw_bounds(self, pieces: List[ScreenPos]):
    #     # TODO fix this to first get hex coord bounds, then convert
    #     (min_x, max_x, min_y, max_y) = self.get_bounds(pieces)
    #     # TODO
    #     return (
    #         min_x - ScreenCell.PAD_LEFT,
    #         max_x + ScreenCell.PAD_RIGHT,
    #         min_y - ScreenCell.PAD_TOP,
    #         max_y + ScreenCell.PAD_BOTTOM,
    #     )

    # TODO if needed make a datastructure for retrieving this sort of
    # info efficiently
    def get_bounds(self, pieces: List[ScreenPos]):

        # # TODO use iterables with all these maps in the correct way
        min_x = reduce(lambda x1, x2: min(x1, x2), map(lambda p: p.x, pieces))

        max_x = reduce(lambda x1, x2: max(x1, x2), map(lambda p: p.x, pieces))

        min_y = reduce(lambda y1, y2: min(y1, y2), map(lambda p: p.y, pieces))

        max_y = reduce(lambda y1, y2: max(y1, y2), map(lambda p: p.y, pieces))

        return (min_x, max_x, min_y, max_y)

    def count_buffer_pieces(self, buffer: list[list[str | None]]):
        # Count number of pieces
        return reduce(
            add,
            [(int(entry) * 0 + 1)
             for row in buffer
                for entry in row
             if entry is not None])


r"""
 \__/  \__/
 /  \__/  \
 \__/  \__/
 /  \__/  \
"""
r"""
 \___/ 2 \___/
 / 2 \___/ 1 \
 \___/ 1 \___/
 /   \___/   \

"""


r"""
                             \___/ 2 \___/
                             / 2 \___/ 1 \
                             \___/ 1 \___/
                             /   \___/   \
player 1 - p:1 a:5 g:1 m:1                                  player 2 - p:1 a:3 s:3 m:1
"""


r"""
player 1:                                                                  player 2:
p:1                             \___/ 2 \___/                                    p:1
a:5                             / 2 \___/ 1 \                                    a:3
g:1                             \___/ 1 \___/                                    m:1
m:1                             /   \___/   \                                    g:1
"""

r"""
player 1:                                                                  player 2:
pillbug:1                       \___/ 2 \___/                              pillbug:1
ant:5                           / 2 \___/ 1 \                                  ant:3
grasshopper:1                   \___/ 1 \___/                             mosquito:1
mosquito:1                      /   \___/   \                          grasshopper:1
"""
