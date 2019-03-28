from pprintpp import pformat
import icdiff
import py

COLOR_OFF = icdiff.color_codes['none']
COLS = py.io.TerminalWriter().fullwidth - 12

def pytest_assertrepr_compare(config, op, left, right):
    if op != '==':
        return

    icdiff_lines = list(icdiff.ConsoleDiff(cols=COLS, tabsize=2).make_table(
        pformat(left, indent=2, width=COLS / 2).splitlines(),
        pformat(right, indent=2, width=COLS / 2).splitlines(),
    ))

    return ['equals failed'] + [f'{COLOR_OFF}{l}' for l in icdiff_lines]
