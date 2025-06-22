

import logging
from dataclasses import dataclass
from time import sleep
from typing import Dict, OrderedDict, cast

import blessed
from blessed import Terminal
from blessed.keyboard import Keystroke, resolve_sequence

from hex.board import Board
from hex.cli.screen_manager import ScreenManager
from hex.cli.templates.template import Template
from hex.cli.utils import new_keystroke
from hex.piece import Piece
from hex.piece_type import PieceType
from hex.player import Player
from hex.position import Position

logging.basicConfig(
    filename="./logs/hex.log",
    encoding="utf-8",
    filemode="a",
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.DEBUG,
)


@dataclass
class Box:
    min_x: int
    min_y: int

    max_x: int
    max_y: int

# TODO use numpy for thse


def term_bounding_box(term: Terminal) -> Box:
    # RESUME
    return Box(0, 0, term.width - 1, term.height - 1)


def term_to_hex_box(box: Box) -> Box:
    num_vert: int = (box.max_y - box.min_y) // Template.HEIGHT
    num_horiz: int = (box.max_x - box.min_x) // Template.WIDTH
    if (num_vert % 2 == 0):
        num_above_orig = (num_vert // 2) - 1
    else:
        num_above_orig = num_vert // 2
    # TODO
    return None


def generate_place_pieces(board: Board):
    # Calc equivalent hex coords box with 0,0,0 in the middle
    for a in range(2):
        for r in range(10):
            for c in range(10):
                piece = Piece(Position(a, c, r),
                              PieceType.NoPiece, Player.Player1)
                board.move(piece, Position(a, c, r))


class CliGame:

    # System Seq Diagram : [MermaidChart: 1d3677c8-35c2-4a64-9971-d59d7e11e9bd]
    # Seq Diagram: [MermaidChart: 0cc01e70-aa53-4810-889d-46c95a7dcfb3]
    def main(self) -> None:

        try:

            term = blessed.Terminal()
            with term.fullscreen(), term.cbreak(), term.hidden_cursor():
                print(term.home + term.clear)
                board = Board()
                mgr = ScreenManager(
                    board, term, debug=True, slow_display=False)

                # Calc term box size

                # term_box = term_bounding_box(term)
                generate_place_pieces(board)
                # TODO also, commit per day

                val = term.inkey(0.1)
                process_and_display(term, mgr, val, force=True)
                while not val is None and val != "q":
                    val = term.inkey(0.1)
                    process_and_display(term, mgr, val)

                    # logging.debug(inkeys)
                    # TODO limit fps using SDL_delay like pygame tick or other delay function, sleep()?
                    # https://www.pygame.org/docs/ref/time.html#pygame.time.Clock.tick
                    # https://github.com/libsdl-org/SDL/blob/aaa5d70efcd48ab0dd6759ac18964333c8c1a95d/src/timer/windows/SDL_systimer.c#L106
                    # https://github.com/libsdl-org/SDL/blob/aaa5d70efcd48ab0dd6759ac18964333c8c1a95d/src/timer/unix/SDL_systimer.c#L138

                # Loop through hex coords and place a new piece on the board at each

                # alter screen cells so that they print the hex coords
                # add a key shortcut to switch with screen space coords, before translation
                # maybe shortcut to show screen space coords after translation too
        except Exception as ex:
            logging.error(msg=ex)
            exit(1)


def process_and_display(term: Terminal, mgr: ScreenManager, ks, force=False) -> None:
    actions_taken = process_keystrokes(term, mgr, ks)
    if actions_taken or force:
        mgr.display()


def process_keystrokes(term: Terminal, mgr: ScreenManager, ks) -> bool:
    actions_taken: bool = False
    actions_taken = actions_taken or mgr.onkey(ks)
    return actions_taken


if __name__ == "__main__":
    CliGame().main()
