import icdiff
from pprintpp import pformat

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
    yellow_on = '\x1b[1;33m'
    color_off = '\x1b[m'
    green_on = '\x1b[1;32m'
    two_diff = (
        f"2: 'the number t{yellow_on}wo{color_off}',"
        f"                    "
        f"2: 'the number t{yellow_on}hree{color_off}',"
    )
    assert two_diff in output
    three_diff = f"{green_on}    6: [1, 2, 3],{color_off}"
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



