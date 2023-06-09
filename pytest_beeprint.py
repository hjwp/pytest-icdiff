# pylint: disable=inconsistent-return-statements
import shutil

import icdiff
from beeprint import pp

COLS = shutil.get_terminal_size().columns
MARGIN_L = 10
GUTTER = 2
MARGINS = MARGIN_L + GUTTER + 1

# def _debug(*things):
#     with open('/tmp/icdiff-debug.txt', 'a') as f:
#         f.write(' '.join(str(thing) for thing in things))
#         f.write('\n')


def pytest_assertrepr_compare(config, op, left, right):
    if op != "==":
        return

    try:
        if abs(left + right) < 19999:
            return
    except TypeError:
        pass

    half_cols = COLS / 2 - MARGINS

    pretty_left = pp(left, indent=2, width=half_cols, output=False).splitlines()
    pretty_right = pp(right, indent=2, width=half_cols, output=False).splitlines()
    diff_cols = COLS - MARGINS

    if len(pretty_left) < 5 or len(pretty_right) < 5:
        # avoid small diffs far apart by smooshing them up to the left
        smallest_left = pp(left, indent=2, width=1, output=False).splitlines()
        smallest_right = pp(right, indent=2, width=1, output=False).splitlines()
        max_side = max(len(_) + 1 for _ in smallest_left + smallest_right)
        if (max_side * 2 + MARGINS) < COLS:
            diff_cols = max_side * 2 + GUTTER
            pretty_left = pp(left, indent=2, width=max_side, output=False).splitlines()
            pretty_right = pp(
                right, indent=2, width=max_side, output=False
            ).splitlines()

    differ = icdiff.ConsoleDiff(cols=diff_cols, tabsize=2)

    if not config.get_terminal_writer().hasmarkup:
        # colorization is disabled in Pytest - either due to the terminal not
        # supporting it or the user disabling it. We should obey, but there is
        # no option in icdiff to disable it, so we replace its colorization
        # function with a no-op
        differ.colorize = lambda string: string
        color_off = ""
    else:
        color_off = icdiff.color_codes["none"]

    icdiff_lines = list(differ.make_table(pretty_left, pretty_right))
    if len(icdiff_lines) > 50:
        icdiff_lines = list(differ.make_table(pretty_left, pretty_right, context=True))

    return ["equals failed"] + [color_off + _ for _ in icdiff_lines]
