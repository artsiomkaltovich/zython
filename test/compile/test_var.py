import re

import pytest

import zython as zn
from zython._compile.zinc import to_str


def test_range_one_arg():
    class MyModel(zn.Model):
        def __init__(self):
            self.a = zn.var(range(100))

    model = MyModel()
    src = model.compile("satisfy")
    assert "var 0..99: a;" in src


def test_slice_model():
    class MyModel(zn.Model):
        def __init__(self):
            self.a = zn.Array([[1, 2, 3], [4, 5, 6]])
            self.b = zn.sum(self.a[:, 2:3])

    model = MyModel()
    result = model.solve_satisfy(verbose=True)
    print(result)


def create_var(name):
    v = zn.var(int)
    v._name = name
    return v


def create_par(name):
    p = zn.par(5)
    p._name = name
    return p


def create_par_array1d(name):
    p = zn.Array(range(5))
    p._name = name
    return p


class TestTypeToStr:

    @pytest.mark.parametrize("r, expected", [(range(100), "0..99"), (range(1, 10), "1..9"), (range(0, 100), "0..99"),
                                             (range(-10, 10), "-10..9"), (range(-10, -9), "-10..-10")])
    def test_range(self, r, expected):
        assert to_str(r) == expected

    def test_range_step(self):
        with pytest.raises(ValueError, match="step other then 1 isn't supported, but it is 2"):
            to_str(range(1, 10, 2))

    @pytest.mark.parametrize("start", (10, 15))
    def test_range_wrong_start(self, start):
        with pytest.raises(ValueError, match=re.escape(f"start({start}) should be smaller then stop(10)")):
            print(to_str(range(start, 10)))

    def test_range_with_expr(self):
        v = create_var("a")
        p = create_par("b")
        assert "(a - 1)..((b + 1) - 1)" == to_str(range(v - 1, p + 1))

    @pytest.mark.parametrize("array, pos, expected", [(create_par_array1d("a"), slice(2, 3), "fdf")])
    def test_slice(self, array, pos, expected):
        assert expected == to_str(array[pos])
