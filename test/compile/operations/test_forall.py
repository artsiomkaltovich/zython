import pytest

import zython as zn


def test_float_range():
    a = zn.Array([1, 2, 3])
    with pytest.raises(ValueError, match="float ranges are not supported as argument"):
        zn.forall(zn.range(1.0), lambda i: a[i] != a[i + 1])
