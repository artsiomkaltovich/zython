import pytest

import zython as zn
from zython._compile.zinc import _get_array_shape_decl, _get_indexes_def


@pytest.mark.parametrize("shape, expected", [((4,), "0..3"), ((3, 3), "0..2, 0..2"),
                                             ((3, 2, 4), "0..2, 0..1, 0..3")])
def test_get_array_shape_decl(shape, expected):
    assert expected == _get_array_shape_decl(shape)


@pytest.mark.parametrize("array, expected",
                         [(zn.Array(zn.var(int), 10), ("i0__ in 0..9", ["i0__"])),
                          (zn.Array(zn.var(int), (1, 5)), ("i0__ in 0..0, i1__ in 0..4", ["i0__", "i1__"])),
                          (zn.Array(zn.var(int), (5, 4, 2)),
                           ("i0__ in 0..4, i1__ in 0..3, i2__ in 0..1", ["i0__", "i1__", "i2__"]))])
def test_get_indexes_def(array, expected):
    assert expected == _get_indexes_def(array)
