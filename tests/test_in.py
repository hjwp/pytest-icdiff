import icdiff
import re
from pprintpp import pformat

YELLOW_ON = '\x1b[1;33m'
COLOR_OFF = '\x1b[m'
GREEN_ON = '\x1b[1;32m'
ANSI_ESCAPE_RE = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -/]*[@-~]')


def test_short_dict(testdir):
    testdir.makepyfile(
        f"""
        def test_one():
            assert "a certain substring" in "some longer text including an uncertain substring"
        """
    )
    output = testdir.runpytest('-vv').stdout.str()
    expected = f"{YELLOW_ON}n un{COLOR_OFF}certain"
    assert expected in output
