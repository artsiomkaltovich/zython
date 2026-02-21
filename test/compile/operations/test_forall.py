import pytest

import zython as zn
from zython._compile.zinc.to_str import to_str


def test_float_range():
    a = zn.Array([1, 2, 3])
    with pytest.raises(ValueError, match="float ranges are not supported as argument"):
        zn.forall(zn.range(1.0), lambda i: a[i] != a[i + 1])


def test_2_arrays():
    a1 = zn.Array(zn.var(range(5)), shape=(5,))
    a1._name = "a1"
    a2 = zn.Array(zn.var(range(5)), shape=(3,))
    a2._name = "a2"
    a = to_str(zn.forall(a1, a2, lambda x, y: x + y < 5))
    assert a == "forall(x in a1, y in a2)(((x + y) < 5))"
