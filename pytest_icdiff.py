from pprintpp import pformat
import icdiff
import py

COLOR_OFF = icdiff.color_codes['none']
COLS = py.io.TerminalWriter().fullwidth - 12

def hacky_whitespace_reduce(l):
    return l.replace('        ', ' ')

def pytest_assertrepr_compare(config, op, left, right):
    if op != '==':
        return

    icdiff_lines = list(icdiff.ConsoleDiff(cols=COLS, tabsize=2).make_table(
        pformat(left, indent=2, width=COLS / 2).splitlines(),
        pformat(right, indent=2, width=COLS / 2).splitlines(),
    ))
    if len(icdiff_lines) == 1:
        icdiff_lines[0] = hacky_whitespace_reduce(icdiff_lines[0])

    return ['equals failed'] + [f'{COLOR_OFF}{l}' for l in icdiff_lines]
