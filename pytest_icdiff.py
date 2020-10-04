# pylint: disable=inconsistent-return-statements
import os
import difflib
from pprintpp import pformat
import icdiff

COLS = os.get_terminal_size().columns
MARGIN_L = 10
GUTTER = 2
MARGINS = MARGIN_L + GUTTER + 1

# def _debug(*things):
#     with open('/tmp/icdiff-debug.txt', 'a') as f:
#         f.write(' '.join(str(thing) for thing in things))
#         f.write('\n')


def get_best_substring(needle, haystack):
    match_length = int(len(needle) * 1.1)
    possible_substrings = [
        haystack[i: match_length + i]
        for i in range(len(haystack) - match_length)
    ]
    if match := difflib.get_close_matches(needle, possible_substrings, n=1):
        return match[0]


def get_pretty_diff_lines(left, right, color_enabled):
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

    if not color_enabled:
        # colorization is disabled in Pytest - either due to the terminal not
        # supporting it or the user disabling it. We should obey, but there is
        # no option in icdiff to disable it, so we replace its colorization
        # function with a no-op
        differ.colorize = lambda string: string

    return list(differ.make_table(pretty_left, pretty_right))


def pytest_assertrepr_compare(config, op, left, right):
    if op not in ('==', 'in'):
        return

    try:
        # early return for small number comparisons
        if abs(left + right) < 19999:
            return
    except TypeError:
        pass

    color_enabled = config.get_terminal_writer().hasmarkup

    coloroff_code = icdiff.color_codes['none'] if color_enabled else ''

    if op == '==':
        diff_lines = get_pretty_diff_lines(left, right, color_enabled)
        return ['equals failed'] + [coloroff_code + l for l in diff_lines]

    if op == 'in' and str(left) == left and str(right) == right:  # string in comparison
        best_match = get_best_substring(left, right)
        if not best_match:
            return
        diff_lines = get_pretty_diff_lines(left, best_match, color_enabled=True)
        return ['in failed. Closest match was:'] + [coloroff_code + l for l in diff_lines]
