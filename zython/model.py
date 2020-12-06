from abc import ABC, abstractmethod
from typing import Optional, List

import minizinc

from zython.var import var
from zython._compile.ir import IR
from zython._compile.zinc import to_zinc
from zython.operations import _Operation


class Model(ABC):
    def solve_satisfy(self, all_solutions=False):
        solver = minizinc.Solver.lookup("gecode")
        model = minizinc.Model()
        model.add_string(self.compile("satisfy"))
        inst = minizinc.Instance(solver, model)
        for name, value in self._ir.vars.items():
            if value.value is not None:
                inst[name] = value.value
        result = inst.solve(all_solutions=all_solutions)
        return result

    @property
    def constraints(self):
        return self._constraints

    @constraints.setter
    def constraints(self, value):
        self._constraints = value

    def compile(self, how_to_solve):
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

    def get_var_attr(self, attr_name: str, attr):
        if not attr_name.startswith("_"):
            if isinstance(attr, var):
                return attr