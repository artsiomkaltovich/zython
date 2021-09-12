import pytest

import zython as zn


def test_float_range():
    class Model(zn.Model):
        def __init__(self, left, right):
            self.center = zn.var(zn.range(left, right))
            self.constraints = [self.center == (left + right) / 2]

    m = Model(1.3, 5.7)
    result = m.solve_satisfy()
    assert result["center"] == pytest.approx(3.5)
