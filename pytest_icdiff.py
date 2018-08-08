from pprintpp import pformat
import icdiff

def pytest_assertrepr_compare(config, op, left, right):
    if op != '==':
        return
    return ['equals failed'] + list(icdiff.ConsoleDiff(tabsize=2).make_table(
        pformat(left, width=40).splitlines(),
        pformat(right, width=40).splitlines(),
    ))
