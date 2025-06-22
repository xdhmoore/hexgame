

from collections import OrderedDict
from typing import cast
from blessed.keyboard import resolve_sequence
from blessed.terminal import Terminal


def new_buffer(size: int) -> list[list[str | None]]:
    return [[None for i in range(size)] for j in range(size)]


def new_keystroke(key: str, term: Terminal):
    return resolve_sequence(key, cast(OrderedDict[str, int], term._keymap), cast(dict[int, str], term._keycodes))

