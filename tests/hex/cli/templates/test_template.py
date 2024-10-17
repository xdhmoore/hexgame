
from unittest.mock import Mock
from hex.cli.templates.template import Template
from hex.piece_type import PieceType

class TestTemplate:
    def test_init(self):

        t = Template.from_type(PieceType.Ant, Mock())

        assert t.DRAWING == [" ___", "/ c \\", "\\___/"]

        assert t.CENTER == (1, 2)
        assert t.PAD_TOP == 1
        assert t.PAD_LEFT == 2
        assert t.PAD_RIGHT == 2
        assert t.PAD_BOTTOM == 1
        assert t.WIDTH == 5
        assert t.HEIGHT == 3