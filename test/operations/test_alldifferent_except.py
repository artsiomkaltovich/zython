from collections import Counter

import pytest

import zython as zn


class TestBothParams:
    def test_ok_none(self):
        zn.alldifferent([0, 2])

    def test_ok_except0(self):
        zn.alldifferent([0, 2], except0=True)

    def test_ok_except_(self):
        zn.alldifferent([0, 2], except_={1, })

    def test_both_not_ok(self):
        with pytest.raises(ValueError, match="Arguments `except0` and `except_` can't be set at the same time"):
            zn.alldifferent([0, 2], except0=True, except_={1, })


class TestExceptTypes:
    # python set is tested by doctest
    def test_zn_set(self):
        class MyModel(zn.Model):
            def __init__(self):
                self.a = zn.Array(zn.var(range(1, 4)), shape=4)
                self.except_ = zn.Set([1, 2, 3])
                self.constraints = [zn.alldifferent(self.a, except_=self.except_), zn.sum(self.a) == 7]
        model = MyModel()
        result = model.solve_satisfy()
        assert Counter(result["a"]) == {3: 1, 2: 1, 1: 2}

    def test_zn_var_set(self):
        with pytest.raises(ValueError, match="Minizinc doesn't support set of var as `except_` argument"):
            zn.alldifferent([1, 2, 3], except_=zn.Set(zn.var(range(3))))
