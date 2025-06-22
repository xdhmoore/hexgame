from typing import List

from blessed import Terminal


class Keys:
    # UP: int = 259
    # DOWN: int = 258
    # LEFT: int = 260
    # RIGHT: int = 261
    # Best I can tell, inkey() only returns meaningful data when it

    @classmethod
    def arrows(cls, term: Terminal) -> list[str]:
        return [term.KEY_LEFT, term.KEY_UP, term.KEY_DOWN, term.KEY_RIGHT, term.l, term.j, term.h, term.k]


# From https://blessed.readthedocs.io/en/stable/keyboard.html
# https://github.com/jquast/blessed/blob/167c34e5268cacb4501418e71e9b926b80dfe077/blessed/keyboard.py#L24
