import pytest

from zython._compile.zinc.to_str import _get_array_shape_decl


@pytest.mark.parametrize("shape, expected", [((4,), "0..3"), ((3, 3), "0..2, 0..2"),
                                             ((3, 2, 4), "0..2, 0..1, 0..3")])
def test_get_array_shape_decl(shape, expected):
    assert expected == _get_array_shape_decl(shape)
