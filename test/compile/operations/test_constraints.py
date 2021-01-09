import pytest
import zython as zn


class TestConstraint:
    all_diff = zn.alldifferent
    count = lambda arg: zn.count(arg, 1) == 3

    def constract_model(self, constraint):
        class model(zn.Model):
            def __init__(self):
                self.a = zn.var(range(3))
                self.b = zn.var(range(3))
                self.c = zn.var(range(3))
                self.constraints = [constraint((self.a, self.b, self.c))]
        return model()

    @pytest.mark.parametrize("constraint", (all_diff, count))
    def test(self, constraint):
        model = self.constract_model(constraint)
        result = model.solve_satisfy()
        result = {result["a"], result["b"], result["c"]}
        print(result)
