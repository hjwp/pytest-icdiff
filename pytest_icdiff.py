# pylint: disable=inconsistent-return-statements
import shutil
from pprintpp import pformat
import icdiff

AUTO_COLS = shutil.get_terminal_size().columns
MARGIN_L = 10
GUTTER = 2
MARGINS = MARGIN_L + GUTTER + 1

# def _debug(*things):
#     with open('/tmp/icdiff-debug.txt', 'a') as f:
#         f.write(' '.join(str(thing) for thing in things))
#         f.write('\n')


def pytest_addoption(parser):
    parser.addoption(
        "--icdiff-cols",
        action="store",
        default=None,
        help="pytest-icdiff:  specify the width of the screen, in case autodetection fails you",
    )
    parser.addoption(
        "--icdiff-show-all-spaces",
        default=False,
        action="store_true",
        help="pytest-icdiff:  color all non-matching whitespace including that which is not needed for drawing the eye to changes.  Slow, ugly, displays all changes",
    )
    parser.addoption(
        "--icdiff-highlight",
        default=False,
        action="store_true",
        help="pytest-icdiff:  color by changing the background color instead of the foreground color.  Very fast, ugly, displays all changes",
    )
    parser.addoption(
        "--icdiff-line-numbers",
        default=False,
        action="store_true",
        help="pytest-icdiff:  generate output with line numbers. Not compatible with the 'exclude-lines' option.",
    )
    parser.addoption(
        "--icdiff-tabsize",
        default=2,
        help="pytest-icdiff:  tab stop spacing",
    )
    parser.addoption(
        "--icdiff-truncate",
        default=False,
        action="store_true",
        help="pytest-icdiff:  truncate long lines instead of wrapping them",
    )
    parser.addoption(
        "--icdiff-strip-trailing-cr",
        default=False,
        action="store_true",
        help="pytest-icdiff:  strip any trailing carriage return at the end of an input line",
    )


def pytest_assertrepr_compare(config, op, left, right):
    if op != "==":
        return

    try:
        if abs(left + right) < 19999:
            return
    except TypeError:
        pass
    except ValueError:
        # ValueErrors are raised when numpy / pandas errors are checked
        # Bail out of generating a diff and use pytest default output
        return

    COLS = int(config.getoption("--icdiff-cols") or AUTO_COLS)
    half_cols = COLS / 2 - MARGINS
    TABSIZE = int(config.getoption("--icdiff-tabsize") or 2)

    pretty_left = pformat(left, indent=TABSIZE, width=half_cols).splitlines()
    pretty_right = pformat(right, indent=TABSIZE, width=half_cols).splitlines()
    diff_cols = COLS - MARGINS

    if len(pretty_left) < 3 or len(pretty_right) < 3:
        # avoid small diffs far apart by smooshing them up to the left
        smallest_left = pformat(left, indent=TABSIZE, width=1).splitlines()
        smallest_right = pformat(right, indent=TABSIZE, width=1).splitlines()
        max_side = max(len(l) + 1 for l in smallest_left + smallest_right)
        if (max_side * 2 + MARGINS) < COLS:
            diff_cols = max_side * 2 + GUTTER
            pretty_left = pformat(left, indent=TABSIZE, width=max_side).splitlines()
            pretty_right = pformat(right, indent=TABSIZE, width=max_side).splitlines()

    differ = icdiff.ConsoleDiff(
        cols=diff_cols,
        show_all_spaces=config.getoption("--icdiff-show-all-spaces"),
        highlight=config.getoption("--icdiff-highlight"),
        line_numbers=config.getoption("--icdiff-line-numbers"),
        tabsize=TABSIZE,
        truncate=config.getoption("--icdiff-truncate"),
        strip_trailing_cr=config.getoption("--icdiff-strip-trailing-cr"),
    )

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
