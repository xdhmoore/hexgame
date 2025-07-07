
import blessed
from blessed.keyboard import Keystroke

from hex.cli.utils import new_keystroke


class TestUtils:

    # These screen_coords match my notes in being (x,y) instead of (y,x) like everything else
    # @pytest.mark.parametrize("hex_coord,screen_coord", screen_with_hex)
    def test_new_keystroke_letter(self):
        term = blessed.Terminal()
        with term.fullscreen(), term.cbreak(), term.hidden_cursor():
            ks: Keystroke = new_keystroke(term, ucs=u'c')

            # TODO left vs right, expected vs actual should be consistent across odebase
            # Expected vs actual - https://stackoverflow.com/questions/2404978/why-are-assertequals-parameters-in-the-order-expected-actual
            assert None == ks.code
            assert None == ks.name
            assert False == ks.is_sequence



    def test_new_keystroke_arrow(self):
        term = blessed.Terminal()
        with term.fullscreen(), term.cbreak(), term.hidden_cursor():
            # up arrow
            ks: Keystroke = new_keystroke(term, ucs=u"\x1b[A")

            assert term.KEY_UP == ks.code
            assert "KEY_UP" == ks.name
            assert True == ks.is_sequence

    def test_new_keystroke_arrow_code(self):
        term = blessed.Terminal()
        with term.fullscreen(), term.cbreak(), term.hidden_cursor():
            # up arrow
            ks: Keystroke = new_keystroke(term, code=term.KEY_UP)

            assert term.KEY_UP == ks.code
            assert "KEY_UP" == ks.name
            assert True == ks.is_sequence

    def test_new_keystroke_arrow_name(self):
        term = blessed.Terminal()
        with term.fullscreen(), term.cbreak(), term.hidden_cursor():
            # up arrow
            ks: Keystroke = new_keystroke(term, name=u'KEY_UP')

            assert term.KEY_UP == ks.code
            assert "KEY_UP" == ks.name
            assert True == ks.is_sequence
