from blessed import Terminal


class Keys:
    # Best I can tell, inkey() only returns meaningful data when it
    @classmethod
    def arrows(cls, term: Terminal):
        return (term.KEY_LEFT, term.KEY_UP, term.KEY_DOWN, term.KEY_RIGHT)


# From https://blessed.readthedocs.io/en/stable/keyboard.html
# https://github.com/jquast/blessed/blob/167c34e5268cacb4501418e71e9b926b80dfe077/blessed/keyboard.py#L24

Keys.UP = 259
Keys.DOWN = 259
Keys.LEFT = 260
Keys.RIGHT = 261
