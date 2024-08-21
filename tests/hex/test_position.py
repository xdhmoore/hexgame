from hex.position import Position


class TestPosition:
    def test_get_adjacent_positions(self):
        pos = Position(0, 0, 0)
        adjacent_positions = pos.get_adjacent_positions()
        assert [(1, -1, 0), (0, 0, 1), (1, 0, 0), (1, 0, -1), (0, 0, -1), (1, -1, -1)]
