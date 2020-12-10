import pytest

from zython.var_par.var import var


def test_simple():
    v = var(range(10, 100))
    assert v.type == range(10, 100)


def test_one_arg():
    v = var(range(100))
    assert v.type == range(100)


def test_step_arg():
    with pytest.raises(ValueError, match="Step values other than 1 are not supported"):
        v = var(range(10, 100, 2))
