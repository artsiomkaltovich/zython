import pytest

import zython as zn


def test_fix_var_for_constraint():
    class MyModel(zn.Model):
        def __init__(self):
            self.a = zn.par(1)
            self.b = zn.var(self.a + 1, 2)

    with pytest.raises(ValueError, match="Can not pass value to constraint"):
        MyModel()
