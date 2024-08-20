import pytest
from hex.cli.screen_position import ScreenPos
from hex.position import Position

screen_with_hex = [
    ((0, 0, 0), (0, 0)),
    ((1, -1, 0), (4, -1)),
    ((1, -1, -1), (0, -2)),
    ((0, 0, -1), (-4, -1)),
    ((0, 0, 1), (4, 1)),
    ((1, 0, 0), (0, 2))
]


class TestScreenPosition:
    # These screen_coords match my notes in being (x,y) instead of (y,x) like everything else
    @pytest.mark.parametrize('hex_coord,screen_coord',screen_with_hex)
    def test_init_screen_pos(self, hex_coord, screen_coord):
        screen_pos = ScreenPos(*hex_coord)
        # See note above
        assert screen_coord == screen_pos.xy
