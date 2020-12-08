from zython._compile.flags import Flag
from zython.operations import constraint
from zython.operations.constraint import Constraint
from zython.var_par.array import _ArrayVar


class IR:
    def __init__(self, model, how_to_solve):
        self.flags = set()
        self._model = model
        self._vars = self._get_vars()
        self._process_constraints(model)
        self._src = None
        self._how_to_solve = how_to_solve

    def _process_constraints(self, model):
        if not hasattr(model, "_constraints"):
            model._constraints = []
        else:
            for index, c in enumerate(model.constraints):
                if isinstance(c, (list, tuple)):
                    self._process_constraint_collection(index, c)
                self._process_one_constraint(c)

    def _process_one_constraint(self, c):
        if isinstance(c, constraint.all_different):
            self.flags.add(Flag.all_different)

    def _process_constraint_collection(self, index, collection):
        prev_constraint = None
        prev_param = None
        step = 0
        for c in collection:
            for param in c.params:
                if isinstance(param, _ArrayVar):
                    if prev_param is None:
                        prev_param = param
                        prev_constraint = c
                    elif self._compare_cycle_op(prev_constraint, c):
                        if not step:
                            step = param.pos - prev_param.pos
                        else:
                            if step != param.pos - prev_param.pos:
                                raise ValueError("different steps are not supported")
                    else:
                        raise ValueError("different operations cycle or collection are not supported!")
                    prev_param = param
            self._process_one_constraint(c)
            prev_constraint = c
        self.constraints[index] = CycleConstrain(prev_param.array, step, prev_param.pos, prev_constraint)

    def _compare_cycle_op(self, op1, op2):
        return (op1.op is op2.op) and self._compare_param_in_cycle(op1, op2)
        pass

    def _compare_param_in_cycle(self, op1, op2):
        for p1, p2 in zip(op1.params, op2.params):
            if isinstance(p1, _ArrayVar) and isinstance(p2, _ArrayVar):
                pass
            elif p1 != p2:
                return False
        return True

    @property
    def vars(self):
        return self._vars

    @property
    def constraints(self):
        return self._model.constraints

    @property
    def how_to_solve(self):
        return self._how_to_solve

    def _get_vars(self):
        result = {}
        for name, attr in vars(self._model).items():
            attr = self._model.get_var_attr(name, attr)
            if attr is not None:
                attr._name = name
                result[name] = attr
        return result


class CycleConstrain(Constraint):
    def __init__(self, array, step, end, op):
        self.array = array
        self.step = step
        self.end = end
        self.op = op.op
        self.params = [f"{array.name}[i__]" if isinstance(p, _ArrayVar) and p.array is array else p
                       for p in op.params]

    def __str__(self):
        # TODO: support step
        return f"forall(i__ in 0..{self.end})({self.op(*self.params)})"
