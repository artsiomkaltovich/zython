import pytest
import zython as zn


class TestConstraint:
    all_diff = zn.alldifferent
    count = lambda arg: zn.count(arg, 1) == 3

    def construct_model(self, constraint):
        class Model(zn.Model):
            def __init__(self):
                self.a = zn.var(range(3))
                self.b = zn.var(range(3))
                self.c = zn.var(range(3))
                self.constraints = [constraint((self.a, self.b, self.c))]
        return Model()

    @pytest.mark.parametrize("constraint, expected", [(all_diff, {0, 1, 2}), (lambda x: zn.count(x, 1) == 3, {1})])
    def test(self, constraint, expected):
        model = self.construct_model(constraint)
        result = model.solve_satisfy()
        result = {result["a"], result["b"], result["c"]}
        assert result == expected

    @pytest.mark.parametrize("low, high, expected", [(3, 6, True), (24, 50, None)])
    def test_ndistinct(self, low, high, expected):
        class Model(zn.Model):
            def __init__(self, low, high):
                self.a = zn.Array(zn.var(range(1, 10)), shape=40)
                self.n = zn.var(range(low, high))
                self.constraints = [zn.ndistinct(self.a) == self.n]

        result = Model(low, high).solve_satisfy()
        if expected is None:
            assert result._solution is None
        else:
            assert low <= result["n"] < high
            assert result["n"] == len(set(result["a"]))

