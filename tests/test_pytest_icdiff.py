import icdiff
from unittest import mock
import pytest
import re
from pprintpp import pformat

YELLOW_ON = '\x1b[1;33m'
COLOR_OFF = '\x1b[m'
GREEN_ON = '\x1b[1;32m'
ANSI_ESCAPE_RE = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -/]*[@-~]')



def test_short_dict(testdir):
    one = {
        1: "the number one",
        2: "the number two",
    }
    two = {
        1: "the number one",
        2: "the number three",
        6: [1, 2, 3]
    }
    testdir.makepyfile(
        f"""
        def test_one():
            assert {one!r} == {two!r}
        """
    )
    output = testdir.runpytest('-vv').stdout.str()
    print(repr(output))
    two_left = "'the number two'"
    two_right = "'the number three'"
    assert two_left in output
    assert two_right in output
    three_diff = "  6: [1, 2, 3],"
    assert three_diff in output


def test_short_dict_with_colorization(testdir):
    one = {
        1: "the number one",
        2: "the number two",
    }
    two = {
        1: "the number one",
        2: "the number three",
        6: [1, 2, 3]
    }
    testdir.makepyfile(
        f"""
        def test_one():
            assert {one!r} == {two!r}
        """
    )
    # Force colorization in py TerminalWriter
    testdir.monkeypatch.setenv('PY_COLORS', '1')
    output = testdir.runpytest('-vv').stdout.str()
    print(repr(output))
    two_left = f"'the number t{YELLOW_ON}wo{COLOR_OFF}'"
    two_right = f"'the number t{YELLOW_ON}hree{COLOR_OFF}'"
    assert two_left in output
    assert two_right in output
    three_diff = f"{GREEN_ON}  6: [1, 2, 3],{COLOR_OFF}"
    assert three_diff in output


def test_long_dict(testdir):
    one = {
        'currency': 'USD',
        'default_UK_warehouse': 'xforce',
        'default_incoterm': 'EXW',
        'name': 'John Doe',
        'payment_term': '30% deposit, 70% balance',
        'reference': '42551456-a1b3-49bd-beed-b168d9a5ac83',
        'website': 'http://megasofas.example.com',
        'main_contact': {
            'city': 'Madeira',
            'country': 'PT',
            'email': 'example@example.com',
            'fax': '012356 789039',
            'mobile': '012356 789039',
            'name': 'Almeida & Filhos - Example, S.A.',
            'phone': '253444802010',
            'postcode': '4815-123',
            'street': "Senhora Test D'Ajuda, 432",
            'street2': 'Moreira de Conegos'
        },
    }
    two = {
        'currency': 'USD',
        'default_UK_warehouse': 'iforce',
        'default_incoterm': 'EXW',
        'freight_forwarder': 'flexport',
        'name': 'John Doe',
        'payment_term': '30% deposit, 70% balance',
        'reference': '42551456-a1b3-49bd-beed-b168d9a5ac83',
        'website': 'http://megasofas.example.com',
        'main_contact': {
            'name': 'Almeida & Filhos - Example, S.A.',
            'email': 'example@example.com',
            'street': "Senhora Test D'Ajuda, 432",
            'street2': 'Moreira de Conegos',
            'postcode': '4815-123',
            'city': 'Madeira',
            'country': 'PT',
            'phone': '253444802010',
            'fax': '012356 789039',
            'mobile': '012356 789039'
        }
    }
    testdir.makepyfile(
        f"""
        def test_two():
            assert {one!r} == {two!r}
        """
    )
    output = testdir.runpytest('-vv', '--color=yes').stdout.str()
    expected_l = f"'default_UK_warehouse': '{YELLOW_ON}x{COLOR_OFF}force'"
    expected_r = f"'default_UK_warehouse': '{YELLOW_ON}i{COLOR_OFF}force'"
    expected_missing = f"{GREEN_ON}  'freight_forwarder': 'flexport',{COLOR_OFF}"
    assert expected_l in output
    assert expected_r in output
    assert expected_missing in output


def test_only_works_for_equals(testdir):
    testdir.makepyfile(
        f"""
        def test_in():
            assert 1 in [2, 3, 4]

        def test_gt():
            assert 1 > 2
        """
    )
    output = testdir.runpytest().stdout.str()
    assert GREEN_ON not in output
    assert YELLOW_ON not in output
    assert COLOR_OFF not in output


def _assert_line_in_ignoring_whitespace(expected, block):
    parts = expected.split()
    for line in block.splitlines():
        if all(part in line for part in parts):
            return True
    assert False, f'could not find {expected} in:\n{block}'


def test_prepends_icdiff_output_lines_with_color_off(testdir):
    one = ['hello', 'hello']
    two = ['bello', 'hella']
    testdir.makepyfile(
        f"""
        def test_thing():
            assert {one!r} == {two!r}
        """
    )
    output = testdir.runpytest('--color=yes').stdout.str()
    expected = list(icdiff.ConsoleDiff().make_table(
        pformat(one, width=1).splitlines(),
        pformat(two, width=1).splitlines(),
    ))
    print('\n'.join(repr(l) for l in output.splitlines()))
    _assert_line_in_ignoring_whitespace(expected[0], output)


def strip_color_codes(s):
    return re.sub(r'\x1b\[[0-9;]*m', '', s)


def test_avoids_single_line_diffs(testdir):
    one = {1: "1", 2: "2"}
    two = {1: "1", 2: "02", 3: "33"}
    testdir.makepyfile(
        f"""
        def test_one():
            assert {one!r} == {two!r}
        """
    )
    output = testdir.runpytest('-vv').stdout.str()
    print(repr(output))
    assert "1: '1',     1: '1'," in strip_color_codes(output)


def test_does_not_break_drilldown_for_int_comparison(testdir):
    testdir.makepyfile(
        """
        def test_a():
            assert len([1, 2, 3]) == len([1, 2])
        """
    )
    output = testdir.runpytest().stdout.str()
    drilldown_expression = 'where 3 = len([1, 2, 3])'
    assert drilldown_expression in output


def test_long_lines_in_comparators_are_wrapped_sensibly_multiline(testdir):
    left = {1: "hello " * 20, 2: 'two'}
    right = {1: "hella " * 20, 2: 'two'}
    testdir.makepyfile(
        f"""
        def test_one():
            assert {left!r} == {right!r}
        """
    )
    output = testdir.runpytest('-vv', '--color=yes').stdout.str()
    comparison_line = next(l for l in output.splitlines() if '1:' in l and "assert" not in l)
    assert comparison_line.count('hell') < 13


def test_long_lines_in_comparators_are_wrapped_sensibly_singleline(testdir):
    left = "hello " * 10
    right = "hella " * 10
    testdir.makepyfile(
        f"""
        def test_one():
            assert {left!r} == {right!r}
        """
    )
    output = testdir.runpytest('-vv', '--color=yes').stdout.str()
    comparison_line = next(
        l for l in output.splitlines()
        if "hell" in l and "assert" not in l
    )
    assert comparison_line.count('hell') < 15


def test_columns_are_calculated_outside_hook(testdir):
    """
    ok for some reason if you get the TerminalWriter width
    inside of the hook it just always returns 80.
    but (bear with me here) if you monkeypatch.setenv(COLUMNS)
    then it _does_ affect the width inside the hook
    (which is where we don't want to measure it)
    but it does _not_ affect the one outside the hook
    (which is the one we want to use).
    """
    left = "hello " * 10
    right = "hella " * 10
    testdir.makepyfile(
        f"""
        def test_one():
            assert {left!r} == {right!r}
        """
    )
    testdir.monkeypatch.setenv('COLUMNS', '50')
    # testdir._method = 'subprocess'
    output = testdir.runpytest(
        '-vv', '--color=yes',
    ).stdout.str()
    comparison_line = next(
        l for l in output.splitlines()
        if 'hell' in l and "assert" not in l
    )
    assert comparison_line.count('hell') > 5


def test_small_numbers_are_specialcased(testdir):
    testdir.makepyfile(
        f"""
        def test_one():
            assert 404 == 400
        """
    )
    output = testdir.runpytest('-vv', '--color=yes').stdout.str()
    assert "assert 404 == 400" in output
    assert "E       assert 404 == 400" in output


def test_larger_numbers_are_sane(testdir):
    testdir.makepyfile(
        f"""
        def test_one():
            assert 123456 == 1234567
        """
    )
    output = testdir.runpytest('-vv', '--color=yes').stdout.str()
    assert f"123456   123456{GREEN_ON}7" in output


def test_really_long_diffs_use_context_mode(testdir):
    testdir.makepyfile(
        f"""
        def test_one():
            one = list(range(100))
            two = list(range(20)) + ["X"] + list(range(20, 50)) + ["Y"] + list(range(53, 100))
            assert one == two
        """
    )
    output = testdir.runpytest('-vv', '--color=yes', '-r=no').stdout.str()
    assert len(output.splitlines()) < 50
    assert "---" in output  # context split marker
