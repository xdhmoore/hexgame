import logging
import re
from dataclasses import dataclass
from functools import reduce
from inspect import cleandoc
from pprint import pprint
from typing import Dict, List

import blessed
from blessed import Terminal
from blessed.keyboard import Keystroke

from hex.board import Board
from hex.cli.keys import Keys
from hex.cli.screen_manager import ScreenManager
from hex.piece import Piece

# TODO
"""
- place
- display text
- move, single player
- setup REST api
- make cli client
- make browser client


# TODO configure this in file shared across main and demos
"""
logging.basicConfig(
    filename="./logs/hex.log",
    encoding="utf-8",
    filemode="a",
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.DEBUG,
)

# TODO mypy
# TODO store game board and operations as numpy array so tensorflow or pytorch can eval fast


class CliGame:
    # System Seq Diagram : [MermaidChart: 1d3677c8-35c2-4a64-9971-d59d7e11e9bd]
    # Seq Diagram: [MermaidChart: 0cc01e70-aa53-4810-889d-46c95a7dcfb3]
    def main(self) -> None:

        try:

            term = blessed.Terminal()
            with term.fullscreen(), term.cbreak(), term.hidden_cursor():
                print(term.home + term.clear)
                board = Board()

                mgr = ScreenManager(board, term)
                first = True

                # piece1 = Piece(None)
                # board.move(piece1, Position(0, 0, 0))
                # TODO try these 3 next:
                # piece1 = Piece(None, PieceType.Queen)
                # board.move(piece1, Position(0, 2, -1))
                # piece2 = Piece(None, PieceType.Ant)
                # board.move(piece2, Position(1, 1, 1))
                # piece3 = Piece(None, PieceType.Grasshopper)
                # board.move(piece3, Position(0, 0, -1))
                key: Keystroke = term.inkey(timeout=0.1)
                # shouldn't what is passed around be type Keystroke
                # https://blessed.readthedocs.io/en/latest/api/keyboard.html#blessed.keyboard.Keystroke
                while not key is None and key.name != "q":  # and key != '':
                    # TODO - best I can tell, inkey() only returns an obj with
                    # a code or a name if it's a non-alphanumeric key, ie an "application key"
                    # arrow keys are with in this, but I will probably want to use reg keys
                    # later
                    try:
                        # if key != None:
                        # TODO implement player turns
                        # TODO move term to __init__(term)
                        # if key and key.code in Keys.arrows(term):
                        #     #logging.debug('key is', key.code)
                        #     logging.debug('should move')
                        #     mgr.move_selector(key)
                        #     # mgr.selector.activate()
                        if (key):
                            logging.debug("acting on key " + (key.name or ""))
                            mgr.onkey(key)

                        mgr.display()
                        key = term.inkey(timeout=5.5)
                    except Exception as ex:
                        logging.error(ex)
                        if (key):
                            logging.debug('%i', key.code)
                        else:
                            logging.debug('None')
                        raise ex
        except Exception as ex:
            logging.error("Error", exc_info=ex)
            exit()

            # x = input()


if __name__ == "__main__":
    CliGame().main()
