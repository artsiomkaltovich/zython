import zython.var_par.types
from zython.solver.console_wrappers import available_solver_tags
from zython.var_par.var import var
from zython.var_par.par import par
from zython.var_par.collections.array import Array
from zython.var_par.collections.set import Set
from zython.operations.functions_and_predicates import exists, forall, sum, alldifferent, circuit, count, min, max,\
    allequal, ndistinct, increasing, decreasing
from zython.model import Model
from zython.result import as_original


range = zython.var_par.types._range
