import pytest

import zython as zn


def test_ok():
    array = zn.Array(zn.var(zn.range(10)), shape=3)
    array._name = "array"
    zn.disjunctive(array, [1, 2, 3])


def test_not_range():
    with pytest.raises(ValueError, match="start_type should be range, but it is <class 'int'>"):
        array = zn.Array(zn.var(int), shape=3)
        array._name = "array"
        zn.disjunctive(array, [1, 2, 3])


def test_bed_start():
    with pytest.raises(
            ValueError,
            match="start of range type of `start_times` arg should be non negative, but it's -5"
    ):
        array=zn.Array(zn.var(zn.range(-5, 19)), shape=3)
        array._name = "array"
        zn.disjunctive(array, [1, 2, 3])
