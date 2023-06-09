import pytest

import pytest_beeprint

pytest_plugins = "pytester"


def pytest_configure(config: pytest.Config):
    pytest_beeprint.COLS = 100
