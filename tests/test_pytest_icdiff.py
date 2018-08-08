import icdiff
from pprintpp import pformat

YELLOW_ON = '\x1b[1;33m'
COLOR_OFF = '\x1b[m'
GREEN_ON = '\x1b[1;32m'

def test_short(testdir):
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
    output = testdir.runpytest().stdout.str()
    two_diff = (
        f"2: 'the number t{YELLOW_ON}wo{COLOR_OFF}',"
        f"                    "
        f"2: 'the number t{YELLOW_ON}hree{COLOR_OFF}',"
    )
    assert two_diff in output
    three_diff = f"{GREEN_ON}    6: [1, 2, 3],{COLOR_OFF}"
    assert three_diff in output


def test_long(testdir):
    one = {
        'currency': 'USD',
        'default_UK_warehouse': 'iforce',
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
    output = testdir.runpytest('-vv').stdout.str()
    expected_lines = icdiff.ConsoleDiff().make_table(
        pformat(one).split('\n'),
        pformat(two).split('\n')
    )
    for l in expected_lines:
        assert l.strip() in output



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
