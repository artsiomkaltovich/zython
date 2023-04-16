import pytest

import zython as zn


class TestWrongType:
    @pytest.mark.parametrize("field", [zn.par, zn.var])
    def test_str(self, field):
        class MyModel(zn.Model):
            def __init__(self):
                self.a = field("aaa")

        with pytest.raises(ValueError, match="aaa is a variable of unsupported type"):
            MyModel()


def test_fix_var_for_constraint():
    class MyModel(zn.Model):
        def __init__(self):
            self.a = zn.par(1)
            self.b = zn.var(self.a + 1, 2)

    with pytest.raises(ValueError, match="Can not pass value to constraint"):
        MyModel()


def test_var_before_path():
    class MyModel(zn.Model):
        def __init__(self):
            self.a = zn.var(int)
            self.b = zn.par(1)
            self.constraints = [self.a == self.b + 1]

    result = MyModel().solve_satisfy()
    assert result["a"] == 2


def test_two_vars():
    class MyModel(zn.Model):
        def __init__(self):
            self.a = zn.par(1)
            self.b = zn.var(int)
            self.c = zn.var(int)
            self.constraints = [self.b == self.a + 1, self.c == self.a * self.b]

    result = MyModel().solve_satisfy()
    assert result["b"] == 2
    assert result["c"] == 2
