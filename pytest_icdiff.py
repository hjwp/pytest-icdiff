import pprint
import icdiff

def pytest_assertrepr_compare(config, op, left, right):
    return list(icdiff.ConsoleDiff().make_table(
        pprint.pformat(left).split('\n'),
        pprint.pformat(right).split('\n')
    ))
