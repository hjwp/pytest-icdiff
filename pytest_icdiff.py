# pylint: disable=inconsistent-return-statements
import py
from pprintpp import pformat
import icdiff

COLS = py.io.TerminalWriter().fullwidth  # pylint: disable=no-member
MARGIN_L = 9
GUTTER = 2
MARGINS = MARGIN_L + GUTTER + 1


def pytest_assertrepr_compare(config, op, left, right):
    if op != '==':
        return

    try:
        if abs(left + right) < 100:
            return
    except TypeError:
        pass

    half_cols = COLS / 2 - MARGINS

    pretty_left = pformat(left, indent=2, width=half_cols).splitlines()
    pretty_right = pformat(right, indent=2, width=half_cols).splitlines()
    diff_cols = COLS - MARGINS

    if len(pretty_left) < 3 or len(pretty_right) < 3:
        # avoid small diffs far apart by smooshing them up to the left
        pretty_left = pformat(left, indent=2, width=1).splitlines()
        pretty_right = pformat(right, indent=2, width=1).splitlines()
        diff_cols = max(len(l) + 1 for l in pretty_left + pretty_right) * 2
        if (diff_cols + MARGINS) > COLS:
            diff_cols = COLS - MARGINS

    differ = icdiff.ConsoleDiff(cols=diff_cols, tabsize=2)

    if not config.get_terminal_writer().hasmarkup:
        # colorization is disabled in Pytest - either due to the terminal not
        # supporting it or the user disabling it. We should obey, but there is
        # no option in icdiff to disable it, so we replace its colorization
        # function with a no-op
        differ.colorize = lambda string: string
        color_off = ''
    else:
        color_off = icdiff.color_codes['none']

    icdiff_lines = list(differ.make_table(pretty_left, pretty_right))

    return ['equals failed'] + [color_off + l for l in icdiff_lines]
