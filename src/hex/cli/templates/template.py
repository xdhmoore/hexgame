import logging
import re
from typing import Dict, Self
from venv import logger

import blessed
from blessed import Terminal

from hex.cli.templates.template_style import TemplateStyle
from hex.piece_type import PieceType
from hex.player import Player

global_term = blessed.Terminal()
DEFAULT_COLOR = global_term.white


class Template:

    # . is replaced by block or whitespace
    # i is replaced by block or _
    # c is replaced by label
    DEFAULT_DRAWING = r"""
         ___
        /.t.\
        \lmr/
    """

    WIDTH: int
    HEIGHT: int

    def __init__(self, **kwargs):
        self.options = kwargs
        self.drawing = kwargs.get('drawing', Template.DEFAULT_DRAWING)
        self.color = kwargs.get('color', None)
        self.default_color = kwargs.get('default_color', DEFAULT_COLOR)
        self.bold_label = kwargs.get('bold_label', False)
        self.bold_lines = kwargs.get('bold_lines', False)
        self.label = kwargs.get('label', 'a')
        self.piece_type = kwargs.get('piece_type', None)

        # TODO reduce the duplication here below andd above
        self.CENTER_CHAR = self.label

        # TODO have multiple ascii drawings for different zoom settings?

        cleaned_lines = [
            line for line in self.drawing.splitlines() if line.strip() != ""
        ]
        # print(cleaned_lines)
        longest_line_length = 5
        num_lines = 3

        # shortest_indent = ...
        # TODO don't compile regex every time
        shortest_indent = min(
            map(
                lambda match: 0 if match is None else len(match.group()),
                [re.compile(r"^\s*").match(line) for line in cleaned_lines],
            )
        )
        # remove shortest indent from each line
        self.DRAWING = [line[shortest_indent:] for line in cleaned_lines]
        # remove whitespace from any line on the right side
        # find coord of c
        for y_idx, line in enumerate(self.DRAWING):
            c_x = line.find("t")
            if c_x != -1:
                self.CENTER = (y_idx, c_x)
                break
        self.PAD_TOP = self.CENTER[0]
        self.PAD_LEFT = self.CENTER[1]
        self.PAD_RIGHT = longest_line_length - self.CENTER[1] - 1
        self.PAD_BOTTOM = num_lines - self.CENTER[0] - 1
        self.WIDTH = self.PAD_LEFT + 1 + self.PAD_RIGHT
        self.HEIGHT = self.PAD_TOP + 1 + self.PAD_BOTTOM

        # TODO we shouldn't have to compute all of the above on every instance

    def draw(self, term, buffer, coords, debug_context, style: TemplateStyle, player: Player):
        for y_idx, line in enumerate(self.DRAWING):
            for x_idx, c in enumerate(line):
                # TODO pass in piece and display different symbol per kind and different color per player
                # TODO handle when piece is at edge of board?
                # TODO could change3 to handle empty strings or spaces better
                if c and c.strip():
                    y = y_idx - self.PAD_TOP + coords[0]
                    x = x_idx - self.PAD_LEFT + coords[1]

                    if y >= len(buffer) \
                            or x >= len(buffer[y]) \
                            or y < 0 \
                            or x < 0:
                        continue
                    # TODO make all user colors in declarative config theme section
                    # try to make a gruvbox
                    is_label = c == 't'
                    if is_label:
                        c = self.CENTER_CHAR

                    # TODO put r on top, c on bottom, and color based on 'a' so that theres more room for r and c
                    is_bottom_edge = c in ['l', 'm', 'r']
                    is_filling = c == '.'

                    if player == Player.Player1:
                        player_color = term.bold_blue
                    else:
                        # player_color = term.antiquewhite4
                        player_color = term.bold_orange

                    if style in [TemplateStyle.Plain]:
                        if is_label:
                            color = player_color
                        else:
                            color = self.default_color
                        if is_bottom_edge:
                            c = '_'
                        if is_filling:
                            c = ' '
                        buffer[y][x] = color + c + term.normal

                    if style == TemplateStyle.Hover or style == TemplateStyle.Targetted:
                        if not is_label:

                            color = term.bold_lawngreen
                        else:
                            color = player_color
                        if is_bottom_edge:
                            c = '_'
                        if is_filling:
                            c = ' '
                        buffer[y][x] = color + c + term.normal

                    if style == TemplateStyle.Selected:
                        if is_bottom_edge or is_filling:
                            c = '█'
                        if not is_label:
                            color = term.bold_lawngreen
                        else:
                            color = player_color + term.on_lawngreen
                        buffer[y][x] = color + c + term.normal

                    if debug_context and style == TemplateStyle.Debug:
                        if is_label:
                            color = player_color
                        else:
                            color = self.default_color

                        if is_label:
                            c = str(debug_context["hex_pos"].a)
                        elif c == 'l':
                            # I can only display single digit values
                            c = str(debug_context["hex_pos"].x % 10)
                        elif c == 'r':
                            c = str(debug_context["hex_pos"].y % 10)
                        elif c == 'm':
                            c = '_'
                        elif is_filling:
                            c = ' '
                        buffer[y][x] = color + c + term.normal

                    # https://fsymbols.com/images/ascii.png
                    # RESUME fix this logic, also initialize template.from_type correctly
                    # everywhere
                    # if is_label:
                    #     if self.bold_label:
                    #         bold_label = term.bold
                    #     else:
                    #         bold_label = ''
                    #     if self.color:
                    #         buffer[y][x] = term.bold(color + c) + term.normal
                    #     else:
                    #         buffer[y][x] = bold_label + c + term.normal
                    # else:
                    #     if self.color:
                    #         buffer[y][x] = color + c + term.normal
                    #     else:
                    #         buffer[y][x] = c

    # TODO make this generic like
    # return cls(label='q', piece_type=self.piece_type default_color=term.khaki1, **overrides)
    # maybe with a separate config struct mapping piece type to lable, default color, etc.
    # TODO parameterize PieceType like PieceType(StrEnum) and add label, color there
    @classmethod
    def from_type(cls, piece_type: PieceType, term: Terminal, **overrides) -> Self:
        match piece_type:
            case PieceType.Ant:
                return cls(label='a', piece_type=PieceType.Ant, default_color=term.firebrick, **overrides)
            case PieceType.Beetle:
                return cls(label='b', piece_type=PieceType.Beetle, default_color=term.aqua, **overrides)
            case PieceType.Grasshopper:
                return cls(label='g', piece_type=PieceType.Grasshopper, default_color=term.webgreen, **overrides)
            case PieceType.Queen:
                return cls(label='q', piece_type=PieceType.Queen, default_color=term.khaki1, **overrides)
            case PieceType.Spider:
                return cls(label='s', piece_type=PieceType.Spider, default_color=term.purple, **overrides)

            case PieceType.Ladybug:
                return cls(label='l', piece_type=PieceType.Ladybug, default_color=term.red, **overrides)
            case PieceType.Mosquito:
                return cls(label='m', piece_type=PieceType.Mosquito, default_color=term.webgreen, **overrides)
            case PieceType.Pillbug:
                return cls(label='p', piece_type=PieceType.Pillbug, default_color=term.webgreen, **overrides)

            case PieceType.NoPiece:
                return cls(label=' ', piece_type=PieceType.NoPiece, default_color=term.white, **overrides)
            case _:
                logging.error(f"Unknown piece type: {piece_type}")
                assert False


_ = Template(label='q', piece_type=PieceType.Queen)
Template.WIDTH = _.WIDTH
Template.HEIGHT = _.HEIGHT
