from enum import Enum, auto, unique

@unique
class PieceType(Enum):

    # TODO replace this with StrEnum and
    # ANT = ("ANT", 3)
    # __init__(self, name, num)

    # Set enum num/value automatically based on new constructor
    # https://stackoverflow.com/a/19300424/356887
    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, num):
        self.num = num

    Ant = 3
    Beetle = 2
    Grasshopper = 3
    Queen = 1
    Spider = 2
    NoPiece = 0

    # Expansions
    Ladybug = 1
    Mosquito = 1
    Pillbug = 1

    #EXPANSIONS = Ladybug | Mosquito | Pillbug

    @property
    def abbr(self):
        return self.name[0].lower()

    @classmethod
    def num_per_player(cls):
        return sum([mem._value_ for mem in cls.__members__.values()])

    @classmethod
    def total_num_pieces(cls) -> int:
        return 2 * cls.num_per_player()
    
piece_counts: set[str] = set()
for pt in list(PieceType):
    if pt.abbr in piece_counts:
        raise TypeError("Found duplicate abbrev, '" + pt.name + "'")
    piece_counts.add(pt.abbr)

