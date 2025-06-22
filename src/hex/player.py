
from enum import Enum


class Player(Enum):
    Player1 = 1
    Player2 = 2

    def next(self):
        if self == Player.Player1:
            return Player.Player2
        else:
            return Player.Player1