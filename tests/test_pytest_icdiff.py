def test_new_summary(testdir):
    testdir.makepyfile(
        """
        def test_one():
            assert {1: 2, 3: 4} == {1:2, 3: 5, 6: 7}
        """
    )
    output = testdir.runpytest().stdout.str()
    assert 'foo' in output

