from pprintpp import pformat
import icdiff

COLOR_OFF = icdiff.color_codes['none']

def hacky_whitespace_reduce(l):
    return l.replace('        ', ' ')

def pytest_assertrepr_compare(config, op, left, right):
    if op != '==':
        return

    icdiff_lines = list(icdiff.ConsoleDiff(tabsize=2).make_table(
        pformat(left, width=40).splitlines(),
        pformat(right, width=40).splitlines(),
    ))
    if len(icdiff_lines) == 1:
        icdiff_lines[0] = hacky_whitespace_reduce(icdiff_lines[0])

    return ['equals failed'] + [f'{COLOR_OFF}{l}' for l in icdiff_lines]
