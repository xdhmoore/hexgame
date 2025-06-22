
from functools import reduce
from math import ceil
from operator import add
from unittest.mock import Mock

import blessed

from hex.cli.templates.template import Template
from hex.cli.templates.template_style import TemplateStyle
from hex.cli.utils import new_buffer
from hex.piece_type import PieceType
from hex.player import Player
from hex.position import Position


class TestTemplate:

    # TODO move all this str/buffer stuff into a new buffer class
    def str_to_buffer(self, strng: str) -> list[list[str | None]]:
        line_length = -1
        buffer = []
        for line in strng.splitlines():

            # Check line lengths are consistent
            if (line_length == -1):
                line_length = len(line)
            else:
                assert line_length == len(line)
            buffer_line = []
            for ch in line:
                buffer_line += [(ch if ch != " " else None)]

            buffer += buffer_line

        return buffer

    def buff_to_str(self, buff: list[list[str | None]]):
        out = ""
        for line in buff:
            for ch in line:
                # None needs to be a space for comparison's sake
                out += (" " if ch is None else ch)
            out += "\n"

        return out

    def compare_buffers(self, buff1: list[list[str | None]], buff2: list[list[str | None]]):
        assert len(buff1) == len(buff2)

        for y_idx, _ in enumerate(buff1):
            assert len(buff1[y_idx]) == len(buff2[y_idx])
            for x_idx, _ in enumerate(buff1[y_idx]):
                assert buff1[y_idx][x_idx] == buff2[y_idx][x_idx]

        return True

    def test_init(self):

        t = Template.from_type(PieceType.Ant, blessed.Terminal())

        assert t.DRAWING == [" ___", "/.t.\\", "\\lmr/"]

        assert t.CENTER == (1, 2)
        assert t.PAD_TOP == 1
        assert t.PAD_LEFT == 2
        assert t.PAD_RIGHT == 2
        assert t.PAD_BOTTOM == 1
        assert t.WIDTH == 5
        assert t.HEIGHT == 3

    def draw_and_assert(self, coords, assert_str):
        term = blessed.Terminal()
        with term.fullscreen(), term.cbreak(), term.hidden_cursor():
            buffer = new_buffer(3)
            temp = Template.from_type(PieceType.Ant, blessed.Terminal())

            temp.draw(term, buffer, coords, None,
                      TemplateStyle.Plain, Player.Player1)

            rendered = self.buff_to_str(buffer)

            assert_str(rendered)

    # When caller attempts to draw outside buffer, template ignores
    def test_draw_top_left(self) -> None:

        def assert_top_left(actual_str):
            assert actual_str == r"""a \
__/
   
"""
        self.draw_and_assert((0, 0), assert_top_left)

    def test_draw_top_right(self) -> None:

        def assert_top_right(actual_str):
            assert actual_str == r"""/ a
\__
   
"""
        self.draw_and_assert((0, 2), assert_top_right)

    def test_draw_bottom_left(self) -> None:

        def assert_bottom_left(actual_str):
            assert actual_str == r"""   
__ 
a \
"""
        self.draw_and_assert((2, 0), assert_bottom_left)

    def test_draw_bottom_right(self) -> None:

        def assert_bottom_right(actual_str):
            assert actual_str == r"""   
 __
/ a
"""
        self.draw_and_assert((2, 2), assert_bottom_right)
