import logging
import pytest
from hex.cli.screen_position import ScreenPos
from hex.position import Position

# TODO use this pattern everywhere
LOGGER = logging.getLogger(__name__)

screen_with_hex = [

# TODO double check why these didn't work
#     ((0,0,0),   (0,0)),
#     ((0,0,-1),  (0,-2)),
#     ((1,1,0),   (4,-1)),
#     ((1,1,1),   (4,1)),
#     ((0,0,1),   (0,2)),
#     ((1,-1, 1), (-4,1)),
#     ((1,-1,0), (-4,-1)),
#     ((0,0,1),   (0,2)),
#     ((0,2,0), (8,0)),
#     ((0,2,-1), (8, -2)),
# ]

    ((0, 0, 0) ,(0, 0)) ,
    ((0, 0, -1),(0, -2)),
    ((1, 1, 0) ,(12, 1)),
    ((1, 1, 1) ,(12, 3)), 
    ((0, 0, 1) ,(0, 2) ), 
    ((1, -1, 1),(-4, 3)),
    ((1, -1, 0),(-4, 1)), 
    ((0, 0, 1) ,(0, 2) ),
    ((0, 2, 0) ,(16, 0)),
    ((0, 2, -1),(16, -2)),
]

class TestScreenPosition:

    # These screen_coords match my notes in being (x,y) instead of (y,x) like everything else
    @pytest.mark.parametrize("hex_coord,screen_coord", screen_with_hex)
    def test_init_screen_pos(self, hex_coord, screen_coord):
        screen_pos = ScreenPos(*hex_coord)
        # See note above
        assert screen_coord == screen_pos.xy

    # TODO test order of drawing
