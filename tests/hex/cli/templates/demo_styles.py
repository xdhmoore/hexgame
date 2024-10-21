

from math import ceil
from typing import List
import blessed
from hex.cli.templates.template import Template
from hex.cli.templates.template_style import TemplateStyle
from hex.piece_type import PieceType
from hex.player import Player

def new_buffer(size: int) -> List[List[str]]:
    return [[None for i in range(size)] for j in range(size)]

def flush_buffer(term, display_buff):
    out: str = "" #term.clear + term.home
    c: str = None
    for y_idx, line in enumerate(display_buff):
        for x_idx, c in enumerate(line):
            if c:
                # TODO there's probably a better way to do this by concatenating the c's in
                # one line first...
                # print(c + "d")
                out += term.move_xy(x_idx, y_idx) + c  # '█'
    print(out, end="", flush=True)
def main():
    term = blessed.Terminal()
    buffer = new_buffer(100)
    temp = Template.from_type(PieceType.Ant, blessed.Terminal())
    temp.draw(term, buffer, (ceil(Template.HEIGHT / 2) + 1, ceil(Template.WIDTH / 2) + 3) , TemplateStyle.Plain, Player.Player1)
    print(term.clear + term.home)
    print("plain:\n\n")
    flush_buffer(term, buffer)
    print('', end="\n\n", flush=True)

    temp = Template.from_type(PieceType.Ant, blessed.Terminal())
    temp.draw(term, buffer, (ceil(Template.HEIGHT / 2) + 1, ceil(Template.WIDTH / 2) + 9) , TemplateStyle.Plain, Player.Player2)
    print(term.clear + term.home)
    print("plain:\n\n")
    flush_buffer(term, buffer)
    print('', end="\n\n", flush=True)

    
    temp = Template.from_type(PieceType.Ant, blessed.Terminal())
    temp.draw(term, buffer, (ceil(Template.HEIGHT / 2) + 6, ceil(Template.WIDTH / 2) + 3) , TemplateStyle.Hover, Player.Player1)
    print("hover:\n\n")
    flush_buffer(term, buffer)
    print('', end="", flush=True)

    temp = Template.from_type(PieceType.Ant, blessed.Terminal())
    temp.draw(term, buffer, (ceil(Template.HEIGHT / 2) + 6, ceil(Template.WIDTH / 2) + 9) , TemplateStyle.Hover, Player.Player2)
    flush_buffer(term, buffer)
    print('', end="", flush=True)

    temp = Template.from_type(PieceType.NoPiece, blessed.Terminal())
    temp.draw(term, buffer, (ceil(Template.HEIGHT / 2) + 9, ceil(Template.WIDTH / 2) + 3) , TemplateStyle.Hover, Player.Player1)
    flush_buffer(term, buffer)
    print('', end="\n\n", flush=True)

    temp = Template.from_type(PieceType.Ant, blessed.Terminal())
    temp.draw(term, buffer, (ceil(Template.HEIGHT / 2) + 14, ceil(Template.WIDTH / 2) + 3) , TemplateStyle.Selected, Player.Player1)
    print("selected:\n\n")
    flush_buffer(term, buffer)
    print('', end="\n\n", flush=True)

    temp = Template.from_type(PieceType.Ant, blessed.Terminal())
    temp.draw(term, buffer, (ceil(Template.HEIGHT / 2) + 14, ceil(Template.WIDTH / 2) + 9) , TemplateStyle.Selected, Player.Player2)
    flush_buffer(term, buffer)
    print('', end="\n\n", flush=True)

    temp = Template.from_type(PieceType.Ant, blessed.Terminal())
    temp.draw(term, buffer, (ceil(Template.HEIGHT / 2) + 19, ceil(Template.WIDTH / 2) + 3) , TemplateStyle.Targetted, Player.Player1)
    print("targetted:\n\n")
    flush_buffer(term, buffer)
    print('', end="\n\n", flush=True)

    temp = Template.from_type(PieceType.Ant, blessed.Terminal())
    temp.draw(term, buffer, (ceil(Template.HEIGHT / 2) + 19, ceil(Template.WIDTH / 2) + 9) , TemplateStyle.Targetted, Player.Player2)
    flush_buffer(term, buffer)
    print('', end="\n\n", flush=True)

    temp = Template.from_type(PieceType.NoPiece, blessed.Terminal())
    temp.draw(term, buffer, (ceil(Template.HEIGHT / 2) + 22, ceil(Template.WIDTH / 2) + 3) , TemplateStyle.Targetted, Player.Player1)
    flush_buffer(term, buffer)
    print('', end="\n", flush=True)

if __name__ == "__main__":
    main()
