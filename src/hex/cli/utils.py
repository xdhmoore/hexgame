

from collections import OrderedDict
from typing import cast
from blessed.keyboard import resolve_sequence, Keystroke
from blessed.terminal import Terminal


def new_buffer(size: int) -> list[list[str | None]]:
    return [[None for i in range(size)] for j in range(size)]


# def new_keystroke(key: str, term: Terminal):
#     return resolve_sequence(
#         key, cast(OrderedDict[str, int], term._keymap),
#         cast(dict[int, str], term._keycodes))


def new_keystroke(term: Terminal, **kwargs):

    seq_to_code = cast(OrderedDict[str, int], term._keymap)
    code_to_name = cast(dict[int, str], term._keycodes)

    ucs= None
    code = None
    name = None

    for key, val in kwargs.items():
        if (key == 'ucs'):
            ucs = val
        if (key == 'code'):
            code = val
        if (key == 'name'):
            name = val

    # cases
    # ucs seq   code    name
    # Y         -       -
    # -         Y       Y

    if ucs != None:
        assert code is None
        assert name is None
        return resolve_sequence(
            ucs, 
            seq_to_code,
            code_to_name
        )
    
    if code != None:
        assert ucs is None
        assert name is None
        for seq, _code in seq_to_code.items():
            if (code == _code):
                ucs = seq
                name = code_to_name[code]
                break

        assert ucs != None
        return Keystroke(ucs, code, name)

    if name != None:
        assert ucs is None
        assert code is None
        for _code, _name in code_to_name.items():
            if (name == _name):
                code = _code
                break
        for seq, _code in seq_to_code.items():
            if (code == _code):
                ucs = seq
                break
        assert ucs != None

        return Keystroke(ucs, code, name)
