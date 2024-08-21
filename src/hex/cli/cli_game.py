from dataclasses import dataclass
from functools import reduce
from typing import Dict, List
from blessed import Terminal
import blessed
from hex.board import Board
from hex.cli.keys import Keys
from hex.cli.screen_manager import ScreenManager
from hex.piece import Piece
from hex.position import Position
from inspect import cleandoc

from pprint import pprint
import logging
import re

# TODO
"""
- place
- display text
- move, single player
- setup REST api
- make cli client
- make browser client

"""
logging.basicConfig(
    filename="./logs/hex.log",
    encoding="utf-8",
    filemode="a",
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
    level=logging.DEBUG,
)

# TODO mypy
# TODO store game board and operations as numpy array so tensorflow or pytorch can eval fast


class CliGame:
    # System Seq Diagram : [MermaidChart: 1d3677c8-35c2-4a64-9971-d59d7e11e9bd]
    # Seq Diagram: [MermaidChart: 0cc01e70-aa53-4810-889d-46c95a7dcfb3]
    def main(self) -> None:
        term = blessed.Terminal()
        with term.fullscreen(), term.cbreak(), term.hidden_cursor():
            print(term.home + term.clear)
            board = Board()

            mgr = ScreenManager(board, term)

            # piece1 = Piece(None)
            # board.move(piece1, Position(0, 0, 0))
            # TODO try these 3 next:
            piece1 = Piece(None)
            board.move(piece1, Position(0, -1, 0))
            piece2 = Piece(None)
            board.move(piece2, Position(0, 0, -1))
            piece3 = Piece(None)
            board.move(piece3, Position(0, 0, 1))
            key = None
            while key != "q":
                # TODO - best I can tell, inkey() only returns an obj with
                # a code or a name if it's a non-alphanumeric key, ie an "application key"
                # arrow keys are with in this, but I will probably want to use reg keys
                # later
                if key != None:
                    # TODO move term to __init__(term)
                    if key.code in Keys.arrows(term):
                        if mgr.selector is None:
                            mgr.init_selector()
                        else:
                            mgr.move_selector(key)

                mgr.display()
                key = term.inkey(timeout=0.5)
            # x = input()


if __name__ == "__main__":
    CliGame().main()
