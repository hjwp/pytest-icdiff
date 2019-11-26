from collections import OrderedDict

from pprintpp import pformat
import icdiff


def pytest_assertrepr_compare(config, op, left, right):
    if op != '==':
        return

    try:
        if abs(left + right) < 100:
            return
    except TypeError:
        pass

    if isinstance(left, OrderedDict) and type(right) is dict:
        left = _convert_to_dict(left)
    if isinstance(right, OrderedDict) and type(left) is dict:
        right = _convert_to_dict(right)

    terminal_writer = config.get_terminal_writer()
    cols = terminal_writer.fullwidth - 12

    wide_left = pformat(left, indent=2, width=cols / 2).splitlines()
    wide_right = pformat(right, indent=2, width=cols / 2).splitlines()
    if len(wide_left) < 3 or len(wide_right) < 3:
        shortest_left = pformat(left, indent=2, width=1).splitlines()
        shortest_right = pformat(right, indent=2, width=1).splitlines()
        cols = max(len(l) for l in shortest_left + shortest_right) * 2
    else:
        cols = max(len(l) for l in wide_left + wide_right) * 2

    pretty_left = pformat(left, indent=2, width=cols / 2).splitlines()
    pretty_right = pformat(right, indent=2, width=cols / 2).splitlines()

    differ = icdiff.ConsoleDiff(cols=cols + 12, tabsize=2)

    if not terminal_writer.hasmarkup:
        # colorization is disabled in Pytest - either due to the terminal not
        # supporting it or the user disabling it. We should obey, but there is
        # no option in icdiff to disable it, so we replace its colorization
        # function with a no-op
        differ.colorize = lambda string: string
        color_off = ''
    else:
        color_off = icdiff.color_codes['none']

    icdiff_lines = list(differ.make_table(pretty_left, pretty_right))

    return ['equals failed'] + [color_off + l for l in icdiff_lines]


def _convert_to_dict(layer):
    """Converts nested ordered dicts to normal dicts"""
    result = layer
    if isinstance(layer, OrderedDict):
        result = dict(layer)
    if isinstance(layer, list):
        return [_convert_to_dict(item) for item in layer]

    try:
        for key, value in result.items():
            result[key] = _convert_to_dict(value)
    except AttributeError:
        pass

    return result
