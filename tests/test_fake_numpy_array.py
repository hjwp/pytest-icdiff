import pytest

from fakes import FakeNumpyArray


def test():
    """
    FakeNumpyArray can be used to trigger a ValueError
    """
    left = FakeNumpyArray([1, 2, 3])
    right = 1

    with pytest.raises(ValueError):
        abs(left + right) < 19999


def test_init():
    """
    FakeNumpyArray can init with a list.
    """
    result = FakeNumpyArray([1, 2, 3])

    assert isinstance(result, FakeNumpyArray)


def test_add():
    """
    FakeNumpyArray returns instance of itself when `+ 1` is applied to it.
    """
    fake = FakeNumpyArray()

    result = fake + 1

    assert isinstance(result, FakeNumpyArray)


def test_abs():
    fake = FakeNumpyArray()

    result = abs(fake)

    assert isinstance(result, FakeNumpyArray)


def test_bool():
    """
    Attempting to use a FakeNumpyArray in a boolean expression raises.
    """
    fake = FakeNumpyArray()

    with pytest.raises(ValueError):
        fake < 19999
