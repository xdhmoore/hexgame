
from dataclasses import dataclass

from hex.piece_type import PieceType


@dataclass
class PieceBankInfo:
    num: int
    type: PieceType


class PieceBank:
    def __init__(self):

        self.bank = {
            PieceType.Ant : PieceBankInfo(num=3, type=PieceType.Ant),
            PieceType.Beetle : PieceBankInfo(num=2, type=PieceType.Beetle),
            PieceType.Grasshopper: PieceBankInfo(num=3, type=PieceType.Grasshopper),
            PieceType.Ladybug: PieceBankInfo(num=1, type=PieceType.Ladybug),
            PieceType.Mosquito: PieceBankInfo(num=1, type=PieceType.Mosquito),
            PieceType.Pillbug: PieceBankInfo(num=1, type=PieceType.Pillbug),
            PieceType.Queen: PieceBankInfo(num=1, type=PieceType.Queen),
            PieceType.Spider: PieceBankInfo(num=4, type=PieceType.Spider),
        }
