import pytest

from zython import var, par, range


def test_simple():
    v = var(range(10, 100))
    assert v.type.start == 10
    assert v.type.stop == 100


def test_one_arg():
    v = var(range(100))
    assert v.type.start == 0
    assert v.type.stop == 100


def test_step_arg():
    with pytest.raises(ValueError, match="Step values other than 1 are not supported"):
        v = var(range(10, 100, 2))


def test_float_start():
    v = var(range(1.3, 10))
    assert v.type.start == pytest.approx(1.3)
    assert v.type.stop == 10


def test_float_stop():
    v = var(range(1, 10.5))
    assert v.type.start == 1
    assert v.type.stop == pytest.approx(10.5)


def test_float_start_and_stop():
    v = var(range(3.14, 10.5))
    assert v.type.start == pytest.approx(3.14)
    assert v.type.stop == pytest.approx(10.5)


@pytest.mark.parametrize("par_val", [4, 4.0])
def test_with_op(par_val):
    x = par(4)
    v = var(range(x, 10))
    assert v.type.start == x
    assert v.type.stop == 10
