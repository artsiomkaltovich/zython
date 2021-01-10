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
            self.start = zn.par(1)
            self.b = zn.sum(self.a[:, self.start + 1:self.start * 3])

    model = MyModel()
    result = model.solve_satisfy(verbose=True)
    assert 9 == result["b"]


def create_var(name):
    v = zn.var(int)
    v._name = name
    return v


def create_par(name):
    p = zn.par(5)
    p._name = name
    return p


def create_array(name, ndims):
    p = zn.Array(zn.var(range(5)), shape=(5,) * ndims)
    p._name = name
    return p


class TestTypeToStr:
    @pytest.mark.parametrize("v, expected", [(create_var("a"), "a"), (create_par("b"), "b"),
                                             (create_array("arr", 2), "arr")])
    def test_var_to_str(self, v, expected):
        assert to_str(v) == expected

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

    @pytest.mark.parametrize("array, pos, expected", [(create_array("z", 3), (1, 2, 3), "z[1, 2, 3]"),
                                                      (create_array("g", 1), 2, "g[2]")])
    def test_indexes(self, array, pos, expected):
        assert to_str(array[pos]) == expected

    # slices with start or stop == None is tested as model in sum tests due to complex minizinc expression
    @pytest.mark.parametrize("array, pos, expected",
                             [(create_array("a", 1), slice(2, 3), "slice_1d(a, [2..2], 0..0)"),
                              (create_array("b", 2), (4, slice(2, 4)), "slice_2d(b, [4..4, 2..3], 0..0, 0..1)"),
                              (create_array("c", 3), (slice(1, 2), 4, slice(2, 4)),
                               "slice_3d(c, [1..1, 4..4, 2..3], 0..0, 0..0, 0..1)")])
    def test_slice(self, array, pos, expected):
        assert expected == to_str(array[pos])

    @pytest.mark.parametrize("collection, expected", [((1, create_array("a", 2)[1, 2], 3, create_par("c")),
                                                       "[1, a[1, 2], 3, c]"),
                                                      ([1, create_par("c") + create_array("a", 2)[1, 2] + 3],
                                                       "[1, ((c + a[1, 2]) + 3)]")
                                                      ])
    def test_tuple_and_list_to_array(self, collection, expected):
        assert to_str(collection) == expected
