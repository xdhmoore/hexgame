import re
from typing import Dict

from blessed import Terminal
from hex.cli.templates.template_style import TemplateStyle
from hex.piece_type import PieceType

class Template:

    # . is replaced by block or whitespace
    # i is replaced by block or _
    # c is replaced by label
    DEFAULT_DRAWING = r"""
         ___
        /.c.\
        \iii/
    """

    def __init__(self, **kwargs):
        self.options = kwargs;
        self.drawing = kwargs.get('drawing', Template.DEFAULT_DRAWING)
        self.color = kwargs.get('color', None)
        self.default_color = kwargs.get('default_color', None)
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
                lambda match: len(match.group()),
                [re.compile(r"^\s*").match(line) for line in cleaned_lines],
            )
        )
        # remove shortest indent from each line
        self.DRAWING = [line[shortest_indent:] for line in cleaned_lines]
        # remove whitespace from any line on the right side
        # find coord of c
        for y_idx, line in enumerate(self.DRAWING):
            c_x = line.find("c")
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


    def draw(self, term, buffer, coords, style: TemplateStyle):
        for y_idx, line in enumerate(self.DRAWING):
            for x_idx, c in enumerate(line):
                # TODO pass in piece and display different symbol per kind and different color per player
                # TODO handle when piece is at edge of board?
                # TODO could change3 to handle empty strings or spaces better
                if c and c.strip():
                    y = y_idx - self.PAD_TOP + coords[0]
                    x = x_idx - self.PAD_LEFT + coords[1]

                    # TODO chagne to handle 3 cases:
                    # - when inside - draw
                    # - when just over - ignore
                    # - when way over - fail
                    OVERFLOW_ALLOWANCE_X = self.WIDTH * 2
                    OVERFLOW_ALLOWANCE_Y = self.HEIGHT * 2
                    if (
                        (y >= len(buffer) + OVERFLOW_ALLOWANCE_Y)
                        or (x >= len(buffer[y]) + OVERFLOW_ALLOWANCE_X)
                        or y <= -OVERFLOW_ALLOWANCE_Y
                        or x <= -OVERFLOW_ALLOWANCE_X
                    ):
                        # If it's not the center of the tile, just ignore if if it's over the edge of the board
                        # but only within an allowance
                        continue
                    is_label = c == 'c'
                    if is_label:
                        c = self.CENTER_CHAR

                    is_bottom_edge = c == 'i'
                    is_filling = c == '.'


                    if style == TemplateStyle.Plain:
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
                            color = self.default_color
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
                            color =  self.default_color
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
                        
                        

    @classmethod
    def from_type(cls, piece_type: PieceType, term: Terminal, **overrides: Dict[str,any]) -> None:
        match piece_type:
            case PieceType.Queen:
                return Template(label='q', piece_type=PieceType.Queen, default_color=term.khaki1,**overrides)
            case PieceType.Ant:
                return Template(label='a', piece_type=PieceType.Ant, default_color=term.firebrick,**overrides)
            case PieceType.Beetle:
                return Template(label='b', piece_type = PieceType.Beetle, default_color=term.aqua, **overrides)
            case PieceType.Spider:
                return Template(label='s', piece_type=PieceType.Spider, default_color=term.purple, **overrides)
            case PieceType.Grasshopper:
                return Template(label='g', piece_type = PieceType.Grasshopper, default_color=term.webgreen, **overrides)
            case PieceType.NoPiece:
                return Template(label=' ', piece_type = PieceType.NoPiece, default_color=term.white, **overrides)
            case _:
                assert False
        

_ = Template(label='q', piece_type=PieceType.Queen)
Template.WIDTH = _.WIDTH
Template.HEIGHT = _.HEIGHT