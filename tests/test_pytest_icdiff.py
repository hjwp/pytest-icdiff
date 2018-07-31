import icdiff
import pprint

def test_short(testdir):
    one = {1: 2, 3: 4}
    two = {1: 2, 3: 5, 6: 7}
    testdir.makepyfile(
        f"""
        def test_one():
            assert {one!r} == {two!r}
        """
    )
    output = testdir.runpytest().stdout.str()
    # assert 'foo' in output
    expected = '\n'.join(icdiff.ConsoleDiff().make_table(
        pprint.pformat(one).split('\n'),
        pprint.pformat(two).split('\n')
    ))
    assert expected in output

def test_long(testdir):
    one = {'currency': 'USD', 'default_UK_warehouse': 'iforce', 'default_incoterm': 'EXW', 'main_contact': {'city': 'Madeira', 'country': 'PT', 'email': 'example@example.com', 'fax': '012356 789039', 'mobile': '012356 789039', 'name': 'Almeida & Filhos - Example, S.A.', 'phone': '253444802010', 'postcode': '4815-123', 'street': "Senhora Test D'Ajuda, 432", 'street2': 'Moreira de Conegos'}, 'name': 'John Doe', 'payment_term': '30% deposit, 70% balance', 'reference': '42551456-a1b3-49bd-beed-b168d9a5ac83', 'website': 'http://megasofas.example.com'}
    two = {'reference': '42551456-a1b3-49bd-beed-b168d9a5ac83', 'name': 'John Doe', 'currency': 'USD', 'payment_term': '30% deposit, 70% balance', 'default_incoterm': 'EXW', 'default_UK_warehouse': 'iforce', 'freight_forwarder': 'flexport', 'website': 'http://megasofas.example.com', 'main_contact': {'name': 'Almeida & Filhos - Example, S.A.', 'email': 'example@example.com', 'street': "Senhora Test D'Ajuda, 432", 'street2': 'Moreira de Conegos', 'postcode': '4815-123', 'city': 'Madeira', 'country': 'PT', 'phone': '253444802010', 'fax': '012356 789039', 'mobile': '012356 789039'}}
    testdir.makepyfile(
        f"""
        def test_one():
            assert {one!r} == {two!r}
        """
    )
    output = testdir.runpytest().stdout.str()
    # assert 'foo' in output
    expected = '\n'.join(icdiff.ConsoleDiff().make_table(
        pprint.pformat(one).split('\n'),
        pprint.pformat(two).split('\n')
    ))
    assert expected in output



