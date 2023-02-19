from abc import ABC
from datetime import timedelta
from typing import List, Optional

import minizinc

from zython._compile.zinc.zinc import to_zinc
from zython.result import Result
from zython._compile.ir import IR
from zython.operations.constraint import Constraint
from zython.var_par.par import par
from zython.var_par.var import var


class Model(ABC):
    """ Base class for user-defined models to solve """
    constraint: List[Constraint]

    def solve_satisfy(
            self,
            *,
            all_solutions=False,
            result_as=None,
            verbose=False,
            solver="gecode",
            optimisation_level: Optional[int] = None,
            n_processes: Optional[int] = None,
            timeout: Optional[timedelta] = None,
            random_seed: Optional[int] = None,
    ):
        """ Finds solution that satisfied constraints, or the error message if the model can't be solved

        Parameters
        ----------
        all_solutions: bool
            If True all solutions will be returned.
            If False only the first solution is returned.
            Default values is False, so the model will return only one solution, as finding all of them can be
            calculation hard
        verbose: bool
            If True the source code of the model will be print to stdout
        solver: str
            Name of the solver, that will look for solution
        optimisation_level: Optional[int] = None
            Optimisation level for minizinc compiler
                - 0: Disable optimisation
                - 1: Single pass optimisation (default)
                - 2: Flatten twice to improve flattening decisions
                - 3: Perform root-node-propagation
                - 4: Probe bounds of all variables at the root node
                - 5: Probe values of all variables at the root node
        n_processes: Optional[int] = None
            Number of processes the solver can use.
            (Only available when the ``-p`` flag is supported by the solver).
        timeout: Optional[timedelta] = None
            Set the time limit for the process of solving the instance.
        random_seed: Optional[int] = None
            Set the random seed for solver.
            (Only available when the ``-r`` flag is supported by the solver).

        Returns
        -------
        Result: Result
            result of the model solution, value of variables can be reached by dict syntax.
        """
        return self._solve(
            "satisfy",
            all_solutions=all_solutions,
            result_as=result_as,
            verbose=verbose,
            solver=solver,
            optimisation_level=optimisation_level,
            n_processes=n_processes,
            timeout=timeout,
            random_seed=random_seed,
        )

    def solve_maximize(
            self,
            eq,
            /,
            *,
            result_as=None,
            verbose=False,
            solver="gecode",
            optimisation_level: Optional[int] = None,
            n_processes: Optional[int] = None,
            timeout: Optional[timedelta] = None,
            random_seed: Optional[int] = None,
    ):
        return self._solve(
            "maximize",
            eq,
            all_solutions=False,
            result_as=result_as,
            verbose=verbose,
            solver=solver,
            optimisation_level=optimisation_level,
            n_processes=n_processes,
            timeout=timeout,
            random_seed=random_seed,
        )

    def solve_minimize(
            self,
            eq,
            /,
            *,
            result_as=None,
            verbose=False,
            solver="gecode",
            optimisation_level: Optional[int] = None,
            n_processes: Optional[int] = None,
            timeout: Optional[timedelta] = None,
            random_seed: Optional[int] = None,
    ):
        return self._solve(
            "minimize",
            eq,
            all_solutions=False,
            result_as=result_as,
            verbose=verbose,
            solver=solver,
            optimisation_level=optimisation_level,
            n_processes=n_processes,
            timeout=timeout,
            random_seed=random_seed,
        )

    def _solve(
            self,
            *how_to_solve,
            all_solutions,
            result_as,
            verbose,
            solver,
            optimisation_level,
            n_processes,
            timeout,
            random_seed,
    ):
        solver = minizinc.Solver.lookup(solver)
        model = minizinc.Model()
        src = self.compile(how_to_solve)
        if verbose:
            print(src)
        model.add_string(src)
        inst = self._create_inst(model, solver)
        for e in self._ir.enums:
            inst[e.__name__] = e
        result: minizinc.Result = inst.solve(
            all_solutions=all_solutions,
            optimisation_level=optimisation_level,
            processes=n_processes,
            timeout=timeout,
            random_seed=random_seed,
        )
        return result_as(result) if result_as else Result(result)

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

    def _get_var_or_par_attr(self, attr_name: str, attr):
        if not attr_name.startswith("_"):
            if isinstance(attr, (var, par)):
                return attr
            if isinstance(attr, Constraint):
                return var(attr)

    def _create_inst(self, model, solver):
        inst = minizinc.Instance(solver, model)
        for name, param in self._ir.pars.items():
            inst[name] = param.value
        for name, param in self._ir.vars.items():
            # minizinc support values passing in data files
            # https://www.minizinc.org/doc-2.6.4/en/modelling.html#real-number-solving
            # so there is need to assign such variables
            if param.value is not None and not isinstance(param.value, Constraint):
                inst[name] = param.value
        return inst
