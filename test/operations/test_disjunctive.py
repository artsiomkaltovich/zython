import zython as zn


def test_ok():
    array = zn.Array(zn.var(zn.range(10)), shape=3)
    array._name = "array"
    zn.disjunctive(array, [1, 2, 3])
