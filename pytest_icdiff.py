from pprintpp import pformat
import icdiff

COLOR_OFF = icdiff.color_codes['none']

def pytest_assertrepr_compare(config, op, left, right):
    if op != '==':
        return
    icdiff_lines = icdiff.ConsoleDiff(tabsize=2).make_table(
        pformat(left, width=40).splitlines(),
        pformat(right, width=40).splitlines(),
    )
    return ['equals failed'] + [f'{COLOR_OFF}{l}' for l in icdiff_lines]
