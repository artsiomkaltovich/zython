import pytest

import zython as zn


class TestOriginal:
    def test_get_attr(self):
        class MyModel(zn.Model):
            def __init__(self):
                self.b = zn.var(int)
                self.constraints = [self.b == 1]

        result = MyModel().solve_satisfy()
        assert result.original["b"] == 1


class TestResultAs:
    def test_none(self):
        class MyModel(zn.Model):
            def __init__(self):
                self.b = zn.var(int)
                self.constraints = [self.b == 1]

        def result_as(arg):
            return 123

        result = MyModel().solve_satisfy(result_as=result_as)
        assert result == 123


class TestLen:
    def test_len1(self):
        class MyModel(zn.Model):
            def __init__(self):
                self.b = zn.var(int)
                self.constraints = [self.b == 1]

        result = MyModel().solve_satisfy()
        assert len(result) == 1

    @pytest.mark.parametrize("all_solutions", [False, True])
    def test_len0(self, all_solutions):
        class MyModel(zn.Model):
            def __init__(self):
                self.b = zn.var(int)
                self.constraints = [self.b ** 2 == -1]

        result = MyModel().solve_satisfy(all_solutions=all_solutions)
        assert len(result) == 0

    def test_all_true(self):
        class MyModel(zn.Model):
            def __init__(self):
                self.a = zn.var(int)
                self.constraints = [self.a ** 2 == 1]

        result = MyModel().solve_satisfy(all_solutions=True)
        assert len(result) == 2

    def test_all_false(self):
        class MyModel(zn.Model):
            def __init__(self):
                self.a = zn.var(int)
                self.constraints = [self.a ** 2 == 1]

        result = MyModel().solve_satisfy(all_solutions=False)
        assert len(result) == 1
