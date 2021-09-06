from minizinc import find_driver

if not find_driver():
    raise RuntimeError("Solver wasn't found, are you sure you specify minizinc folder to $PATH environment variable")


import zython.var_par.types
from zython.var_par.var import var
from zython.var_par.par import par
from zython.var_par.array import Array
from zython.operations.functions_and_predicates import exists, forall, sum, alldifferent, circuit, count, min, max,\
    allequal, ndistinct, increasing, decreasing
from zython.model import Model
from zython.result import as_original

import builtins

builtins.range = zython.var_par.types._range
