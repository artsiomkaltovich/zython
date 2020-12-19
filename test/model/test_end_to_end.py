import minizinc
import zython
from zython.var_par.var import var


def test_minizinc_example():
    def minizinc_model():
        src = "var int: a;\n" \
              "var int: b;\n" \
              "var int: c;\n" \
              "var -100..100: x;\n" \
              "constraint a == 1;\n" \
              "constraint b == 4;\n" \
              "constraint c == 0;\n" \
              "constraint ((((a * pow(x, 2)) + (b * x)) + c) = 0);\n" \
              "solve satisfy"
        model = minizinc.Model()
        model.add_string(src)
        gecode = minizinc.Solver.lookup("gecode")
        inst = minizinc.Instance(gecode, model)
        result = inst.solve(all_solutions=True)
        return result

    def model():
        class MyModel(zython.Model):
            def __init__(self, a: int, b: int, c: int):
                self.a = var(a)
                self.b = var(b)
                self.c = var(c)
                self.x = var(range(-100, 101))
                self.constraints = [self.a * self.x ** 2 + self.b * self.x + self.c == 0]

        model = MyModel(1, 4, 0)
        result = model.solve_satisfy(all_solutions=True, result_as=zython.as_original)
        return model.src, result

    expected_result = minizinc_model()
    actual_src, actual_result = model()
    assert str(expected_result) == str(actual_result)
    assert "constraint ((((a * pow(x, 2)) + (b * x)) + c) == 0);" in actual_src
    assert "var -100..100: x;" in actual_src
    assert "solve satisfy" in actual_src


def test_range_cmp():
    def minizinc_model(limits):
        result = []
        for a, b in limits:
            src = "var int: a;\n" \
                  "var int: b;\n" \
                  "var -100..100: x;\n" \
                  f"constraint a == {a};\n" \
                  f"constraint b == {b};\n" \
                  "constraint a < x;\n" \
                  "constraint x < b;\n" \
                  "solve satisfy"
            model = minizinc.Model()
            model.add_string(src)
            gecode = minizinc.Solver.lookup("gecode")
            inst = minizinc.Instance(gecode, model)
            result.append(inst.solve(all_solutions=True))
        return result

    def model(limits):
        class MyModel(zython.Model):
            def __init__(self, a: int, b: int):
                self.a = var(a)
                self.b = var(b)
                self.x = var(range(-100, 101))
                self.constraints = [self.a < self.x, self.x < self.b]

        result = []
        for a, b in limits:
            model = MyModel(a, b)
            result.append(model.solve_satisfy(all_solutions=True, result_as=zython.as_original))
        return result

    limits = [(1, 4), (-200, -94), (99, 105), (200, 503)]
    expected_result = minizinc_model(limits)
    actual_result = model(limits)
    assert len(expected_result) == len(actual_result)
    assert all(str(e.solution) == str(a.solution) for e, a in zip(expected_result, actual_result))
    assert len(expected_result[2].solution) == 1
    assert len(actual_result[2].solution) == 1
