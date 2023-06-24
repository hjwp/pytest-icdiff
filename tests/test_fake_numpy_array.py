import pytest

from fakes import FakeNumpyArray


@pytest.fixture
def fake():
    return FakeNumpyArray([1, 2, 3])


# --- INTEGRATED ---


def test_in_test(fake):
    """
    FakeNumpyArray can be used to equate to False in a test assertion, this
    means this fake can be used to trigger pytest to try to generate a diff
    (gets us into this plugin's code).
    """
    result = all(fake == 2)

    assert result is False


def test_in_icdiff(fake):
    """
    A FakeNumpyArray instance will trigger a ValueError when pytest-icdiff
    checks it before diffing.
    """
    left = FakeNumpyArray([1, 2, 3])
    right = 1

    with pytest.raises(ValueError):
        abs(left + right) < 19999


# --- PARTS ---


def test_init(fake):
    """
    FakeNumpyArray can init with a list.
    """
    result = fake

    assert isinstance(result, FakeNumpyArray)


def test_eq(fake):
    """
    FakeNumpyArray returns instance of itself when `==` is applied to it.
    """
    result = fake == 1

    assert isinstance(result, FakeNumpyArray)


def test_add(fake):
    """
    FakeNumpyArray returns instance of itself when `+ 1` is applied to it.
    """
    result = fake + 1

    assert isinstance(result, FakeNumpyArray)


def test_abs(fake):
    result = abs(fake)

    assert isinstance(result, FakeNumpyArray)


def test_bool(fake):
    """
    Attempting to use a FakeNumpyArray in a boolean expression raises.
    """
    with pytest.raises(ValueError):
        fake < 19999
