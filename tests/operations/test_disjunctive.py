import pytest
import zython as zn


@pytest.mark.parametrize("array", [(1, 2, 3), ((1, 2, 3), (1, 2, 3)), zn.Array(zn.var(zn.range(10)), shape=3)])
def test_ok(array):
    array = zn.Array(zn.var(zn.range(10)), shape=3)
    array._name = "array"
    zn.disjunctive(array, array)
