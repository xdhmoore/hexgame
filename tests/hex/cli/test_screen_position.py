import pytest
from hex.cli.screen_position import ScreenPos
from hex.position import Position


class TestScreenPosition:
    @pytest.mark.parametrize('hex_coord,screen_coord', [
        ((0, 0, 0), (0, 0)),
        ((1, -1, 0), (4, -1)),
        ((1, -1, -1), (0, -2)),
        ((0, 0, -1), (-4, -1)),
        ((0, 0, 1), (4, 1)),
        ((1, 0, 0), (0, 2))
    ])
    def test_init_screen_pos(self, hex_coord, screen_coord):
        screen_pos = ScreenPos(*hex_coord)
        assert screen_coord == screen_pos.xy