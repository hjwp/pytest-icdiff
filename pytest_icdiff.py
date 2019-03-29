from pprintpp import pformat
import icdiff
import py

COLOR_OFF = icdiff.color_codes['none']
COLS = py.io.TerminalWriter().fullwidth - 12

def pytest_assertrepr_compare(config, op, left, right):
    if op != '==':
        return

    wide_left = pformat(left, indent=2, width=COLS / 2).splitlines()
    wide_right = pformat(right, indent=2, width=COLS / 2).splitlines()
    if len(wide_left) < 3 or len(wide_right) < 3:
        shortest_left = pformat(left, indent=2, width=1).splitlines()
        shortest_right = pformat(right, indent=2, width=1).splitlines()
        cols = max(len(l) for l in shortest_left + shortest_right) * 2
    else:
        cols = max(len(l) for l in wide_left + wide_right) * 2

    pretty_left = pformat(left, indent=2, width=cols / 2).splitlines()
    pretty_right = pformat(right, indent=2, width=cols / 2).splitlines()


    icdiff_lines = list(icdiff.ConsoleDiff(cols=cols + 12, tabsize=2).make_table(
        pretty_left, pretty_right
    ))

    return ['equals failed'] + [f'{COLOR_OFF}{l}' for l in icdiff_lines]
