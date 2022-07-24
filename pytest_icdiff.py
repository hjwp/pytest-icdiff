# pylint: disable=inconsistent-return-statements
import shutil
from pprintpp import pformat
import icdiff

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

    pretty_left = pformat(left, indent=2, width=half_cols).splitlines()
    pretty_right = pformat(right, indent=2, width=half_cols).splitlines()
    diff_cols = COLS - MARGINS

    if len(pretty_left) < 3 or len(pretty_right) < 3:
        # avoid small diffs far apart by smooshing them up to the left
        smallest_left = pformat(left, indent=2, width=1).splitlines()
        smallest_right = pformat(right, indent=2, width=1).splitlines()
        max_side = max(len(l) + 1 for l in smallest_left + smallest_right)
        if (max_side * 2 + MARGINS) < COLS:
            diff_cols = max_side * 2 + GUTTER
            pretty_left = pformat(left, indent=2, width=max_side).splitlines()
            pretty_right = pformat(right, indent=2, width=max_side).splitlines()

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

    return ["equals failed"] + [color_off + l for l in icdiff_lines]
