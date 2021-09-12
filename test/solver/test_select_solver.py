import minizinc
import pytest

import zython as zn


def test_select_solver():
    def minizinc_model():
        src = "float: a;\n" \
              "var float: x;\n" \
              "constraint x == a + 1;\n" \
              "solve satisfy"
        model = minizinc.Model()
        model.add_string(src)
        solver = minizinc.Solver.lookup("cbc")
        inst = minizinc.Instance(solver, model)
        inst["a"] = 2
        result = inst.solve()
        return result

    def model():
        class Model(zn.Model):
            def __init__(self, a):
                self.a = zn.par(a)
                self.x = zn.var(float)
                self.constraints = [self.x == self.a + 1]

        m = Model(2.0)
        return m.solve_satisfy(solver="cbc")

    expected_result = minizinc_model()
    actual_result = model()
    assert pytest.approx(expected_result["x"]) == actual_result["x"]
