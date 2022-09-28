from datetime import timedelta

import minizinc
import zython
from zython import var
from zython.var_par.par import par


def test_minizinc_example():
    def minizinc_model():
        src = "int: a;\n" \
              "int: b;\n" \
              "int: c;\n" \
              "var -100..100: x;\n" \
              "constraint ((((a * pow(x, 2)) + (b * x)) + c) = 0);\n" \
              "solve satisfy"
        model = minizinc.Model()
        model.add_string(src)
        gecode = minizinc.Solver.lookup("gecode")
        inst = minizinc.Instance(gecode, model)
        inst["a"] = 1
        inst["b"] = 4
        inst["c"] = 0
        result = inst.solve(all_solutions=True)
        return result

    def model():
        class MyModel(zython.Model):
            def __init__(self, a: int, b: int, c: int):
                super().__init__()
                self.a = par(a)
                self.b = par(b)
                self.c = par(c)
                self.x = var(range(-100, 101))
                self.constraints = [self.a * self.x ** 2 + self.b * self.x + self.c == 0]

        model = MyModel(1, 4, 0)
        result = model.solve_satisfy(all_solutions=True, result_as=zython.as_original)
        return model.src, result

    expected_result = minizinc_model()
    actual_src, actual_result = model()
    assert str(expected_result.solution) == str(actual_result.solution)  # minizinc doesn't support solution eq
    assert "constraint ((((a * pow(x, 2)) + (b * x)) + c) == 0);" in actual_src
    assert "var -100..100: x;" in actual_src
    assert "solve satisfy" in actual_src


def test_range_cmp():
    def minizinc_model():
        src = "int: a;\n" \
              "int: b;\n" \
              "var -100..100: x;\n" \
              "constraint a < x;\n" \
              "constraint x < b;\n" \
              "solve satisfy"
        model = minizinc.Model()
        model.add_string(src)
        gecode = minizinc.Solver.lookup("gecode")
        inst = minizinc.Instance(gecode, model)
        inst["a"] = 1
        inst["b"] = 4
        result = inst.solve(all_solutions=True)
        return result

    def model():
        class MyModel(zython.Model):
            def __init__(self, a: int, b: int):
                super().__init__()
                self.a = par(a)
                self.b = par(b)
                self.x = var(range(-100, 101))
                self.constraints = [self.a < self.x, self.x < self.b]

        model = MyModel(1, 4, )
        result = model.solve_satisfy(all_solutions=True, result_as=zython.as_original)
        return result

    expected_result = minizinc_model()
    actual_result = model()
    assert str(expected_result) == str(actual_result)


def test_extra_solve_args():
    def model():
        class MyModel(zython.Model):
            def __init__(self, a: int, b: int):
                super().__init__()
                self.a = par(a)
                self.b = par(b)
                self.x = var(range(-100, 101))
                self.constraints = [self.a < self.x, self.x < self.b]

        model = MyModel(1, 4, )
        result = model.solve_satisfy(
            optimisation_level=2,
            n_processes=3,
            timeout=timedelta(seconds=4),
            random_seed=5,
        )
        return result

    actual_result = model()
    assert actual_result
