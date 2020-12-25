from abc import ABC

import minizinc

from zython.result import Result
from zython._compile.ir import IR
from zython._compile.zinc import to_zinc
from zython.operations.constraint.constraint import Constraint
from zython.var_par.par import par
from zython.var_par.var import var


class Model(ABC):
    """ Base class for user-defined models to solve """

    def solve_satisfy(self, all_solutions=False, result_as=None):
        """ Finds solution that satisfied constraints, or the error message if the model can't be solved

        Parameters
        ----------
        all_solutions: bool
            If True all solutions will be returned.
            If False only the first solution is returned.
            Default values is False, so the model will return only one solution, as finding all of them can be
            calculation hard

        Returns
        -------
        Result: Result
            result of the model solution, value of variables can be reached by dict syntax.
        """
        solver = minizinc.Solver.lookup("gecode")
        model = minizinc.Model()
        model.add_string(self.compile("satisfy"))
        inst = minizinc.Instance(solver, model)
        for name, par in self._ir.pars.items():
            inst[name] = par.value
        result = inst.solve(all_solutions=all_solutions)
        if result_as is None:
            return Result(result)
        else:
            return result_as(result)

    @property
    def constraints(self):
        return self._constraints

    @constraints.setter
    def constraints(self, value):
        self._constraints = value

    def compile(self, how_to_solve="satisfy"):
        if not hasattr(self, "_ir"):
            self._ir = IR(self, how_to_solve)
            result = to_zinc(self._ir)
            self._src = result
        assert self._src, "Model wasn't compiled"
        return self._src

    @property
    def src(self):
        assert hasattr(self, "_src"), "Please solve or compile first"
        return self._src

    def _get_var_or_par_attr(self, attr_name: str, attr):
        if not attr_name.startswith("_"):
            if isinstance(attr, (var, par)):
                return attr
            if isinstance(attr, Constraint):
                return par(attr)
