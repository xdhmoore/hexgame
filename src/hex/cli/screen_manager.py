
from __future__ import annotations

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
from hex.cli import piece_bank_manager
from hex.cli.keys import Keys
from hex.cli.piece_bank_manager import PieceBankManager
from hex.cli.screen_cell import ScreenCell
from hex.cli.screen_position import ScreenPos
from hex.cli.selector_cell import SelectorCell
from hex.cli.state.abstract import AbstractState, StateType
from hex.cli.state.pick_piece_type import PickPieceTypeState
from hex.cli.templates.template import Template
from hex.cli.templates.template_style import TemplateStyle
from hex.piece import Piece
from hex.piece_type import PieceType
from hex.player import Player
from hex.position import Position


@dataclass
class PlayerDisplayState:
    piece_bank_mgr: PieceBankManager
    # selected_piece: Piece | None = None

# TODO put all these handler classes in their own file


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
        self.state: AbstractState = PickPieceTypeState(term, board)
        self.selected_type: None | PieceType = None

        self.view_offset: tuple[int, int] = (0, 0)

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
        return [ScreenCell(self.term, (TemplateStyle.Debug if self.debug else TemplateStyle.Plain),  node.piece) for node in self.board.map.mapmap.values()]

    # TODO hwo to do javadocs for methods, cclasses, etc
    # returns whether any action was taken that might need a redraw
    def on_key(self, key: Keystroke):
        actions_taken = False
        next_state, actions_taken = self.state.on_key(key, self)
        if (next_state):
            self.state = next_state

        return (next_state, actions_taken)
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
        # str_piece_bank = self.piece_bank_mgr1.draw(Player.Player1, PieceType
        self.player_display_state_map[Player.Player1].piece_bank_mgr.draw(
            self.display_buff)
        self.player_display_state_map[Player.Player2].piece_bank_mgr.draw(
            self.display_buff)

    def draw_pieces(self) -> None:
        self.draw_cells(self.cells)

    def draw_selector(self) -> None:
        if self.selector:
            self.draw_cells([self.selector])

    # TODO Make more typing mandatory -> Stuff
    def draw_cells(self, screen_cells) -> None:
        """Draws pieces and selector"""


        for screen_cell in reversed(screen_cells):
            if self.slow_display:
                time.sleep(0.2)
            screen_cell.draw(term=self.term,
                             buffer=self.display_buff,
                             player=Player.Player1,  # TODO update when turns implemented
                             viewport_offset=self.get_viewport_offset())
            if self.slow_display:
                self.flush_buffer()

    # TODO right now this functions as the viewport but at some point will want to make the viewport moveable
    def get_viewport_offset(self) -> tuple[int, int]:
        screen_center = self.get_screen_center()

        return (
            screen_center[0] + self.view_offset[0],
            screen_center[1] + self.view_offset[1]
        )

    # TODO change this to offset within player areas
    def get_screen_center(self) -> tuple[int, int]:
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

    def get_piece_bank_selected(self) -> tuple[Player, PieceType]:
        display_state: PlayerDisplayState = self.player_display_state_map[self.board.curr_player]
        return (self.board.curr_player, display_state.piece_bank_mgr.current_piece)

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
        out: str = self.term.clear + self.term.home
        c: str | None = None
        for y_idx, line in enumerate(self.display_buff):
            for x_idx, c in enumerate(line):
                if c:
                    # TODO there's probably a better way to do this by concatenating the c's in
                    # one line first...
                    # print(c + "d")
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
