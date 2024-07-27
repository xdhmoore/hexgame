from dataclasses import dataclass
from functools import reduce
from typing import Dict, List
from blessed import Terminal
import blessed
from hex.board import Board
from hex.cli.screen_position import ScreenPos
from hex.piece import Piece
from hex.position import Position

from inspect import cleandoc

import logging
import re

# TODO
'''
- place
- display text
- move, single player
- setup REST api
- make cli client
- make browser client

'''
logging.basicConfig(
    filename="hex.log",
    encoding="utf-8",
    filemode="a",
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
    level=logging.DEBUG
)

NUM_PIECES_PER_TEAM = 11


class Cell:

    @classmethod
    def draw(cls, buffer, screen_coords):
        for y_idx, line in enumerate(cls.DRAWING):
            for x_idx, c in enumerate(line):
                # TODO pass in piece and display different symbol per kind and different color per player
                if c:
                    buffer[x_idx - cls.PAD_LEFT][y_idx - cls.PAD_TOP] = c

    @classmethod
    def init_class(cls):
        raw_drawing = r"""
             ___ 
            / c \
            \___/
        """

        cleaned_lines = [line for line in raw_drawing.splitlines()
                         if line.strip() != '']
        print(cleaned_lines)
        longest_line_length = 5
        num_lines = 3

        # shortest_indent = ...
        # TODO don't compile regex every time
        shortest_indent = min(map(lambda match: len(match.group()), [
                              re.compile(r'^\s*').match(line) for line in cleaned_lines]))
        # remove shortest indent from each line
        cls.DRAWING = [line[shortest_indent:] for line in cleaned_lines]
        # remove whitespace from any line on the right side
        # find coord of c
        for y_idx, line in enumerate(cls.DRAWING):
            c_x = line.find('c')
            if c_x is not None:
                cls.CENTER = (c_x, y_idx)
                break
        cls.PAD_TOP = cls.CENTER[1]
        cls.PAD_LEFT = cls.CENTER[0]
        cls.PAD_RIGHT = longest_line_length - cls.CENTER[0]
        cls.PAD_BOTTOM = num_lines - cls.CENTER[1] - 1
        cls.WIDTH = cls.PAD_LEFT + 1 + cls.PAD_RIGHT
        cls.HEIGHT = cls.PAD_TOP + 1 + cls.PAD_BOTTOM


Cell.init_class()
# TODO mypy
# TODO store game board and operations as numpy array so tensorflow or pytorch can eval fast


class CliGame:

    def main(self) -> None:
        term = blessed.Terminal()
        with term.fullscreen(), term.cbreak(), term.hidden_cursor():
            print(term.home + term.clear)
            board = Board()
            piece1 = Piece(None)
            board.move(piece1, Position(0, -1, 0))
            piece2 = Piece(None)
            board.move(piece2, Position(0, 0, -1))
            piece3 = Piece(None)
            board.move(piece3, Position(0, 0, 1))
            while term.inkey(timeout=0.02) != 'q':
                self.display(term, board)

    # TODO if needed
    # def on_resize

    # TODO redo all this and use numpy
    def get_screen_center(self, term: Terminal):
        return (term.width // 2, term.height // 2)

    def display_space(self, term, screen_pos: ScreenPos, ch):
        screen_coord = (
            self.get_screen_center(term)[0] + screen_pos.x,
            self.get_screen_center(term)[1] + screen_pos.y
        )

        Cell.draw(self.display_buff, screen_coord)
        # self.display_buff[screen_coord[1], screen_coord[0]] = ch

    def display(self, term: Terminal, board: Board) -> None:
        pieces = map(lambda piece: (piece, ScreenPos(piece.pos)),
                     board.pieces.values())

        # TODO use iterables with all these maps in the correct way
        bounds = self.get_draw_bounds(list(map(lambda tup: tup[1], pieces)))

        # TODO make 2d buffer covering board
        # Room to start at origin with 1 and put all the pieces down in a line in any single direction
        self.clear_display_buff()
        print(term.clear, end='', flush=True)
        chars = ('O', 'C', 'H', 'R')
        c = 0
        for piece in board.pieces.values():
            logging.debug(f'display piece at {ScreenPos(piece.pos)}')
            self.display_space(term, ScreenPos(piece.pos), chars[c])
            c += 1

        self.flush_buffer(term)
        return

    def clear_display_buff(self):
        display_buff_width = NUM_PIECES_PER_TEAM * 4 * Cell.WIDTH + 1
        display_buff_height = NUM_PIECES_PER_TEAM * 4 * Cell.HEIGHT + 1
        self.display_buff = [[None for i in range(
            display_buff_width)] for j in range(display_buff_height)]

    def flush_buffer(self, term: Terminal):
        out: str = term.clear + term.home
        c: str = None
        for y_idx, line in enumerate(self.display_buff):
            for x_idx, c in enumerate(line):
                if (c):
                    # TODO there's probably a better way to do this by concatenating the c's in
                    # one line first...
                    print(c + "d")
                    # out += term.move_xy(x_idx, y_idx) + '█' + c
        print(out, end='', flush=True)
        self.clear_display_buff()

    def get_draw_bounds(self, pieces: List[ScreenPos]):
        (min_x, max_x, min_y, max_y) = self.get_bounds(pieces)
        # TODO
        return (
            min_x - Cell.PAD_LEFT,
            max_x + Cell.PAD_RIGHT,
            min_y - Cell.PAD_TOP,
            max_y + Cell.PAD_BOTTOM
        )

    # TODO if needed make a datastructure for retrieving this sort of
    # info efficiently
    def get_bounds(self, pieces: List[ScreenPos]):

        min_x = reduce(lambda x1, x2: min(x1, x2), map(lambda p: p.x, pieces))

        max_x = reduce(lambda x1, x2: max(x1, x2), map(lambda p: p.x, pieces))

        min_y = reduce(lambda y1, y2: min(y1, y2), map(lambda p: p.y, pieces))

        max_y = reduce(lambda y1, y2: max(y1, y2), map(lambda p: p.y, pieces))

        return (
            min_x,
            max_x,
            min_y,
            max_y
        )


r'''
 \__/  \__/
 /  \__/  \
 \__/  \__/
 /  \__/  \
'''
r'''
 \___/ 2 \___/
 / 2 \___/ 1 \
 \___/ 1 \___/
 /   \___/   \

'''


if __name__ == '__main__':
    CliGame().main()
