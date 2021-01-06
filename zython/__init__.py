import zython.var_par.types
from zython.var_par.var import var
from zython.var_par.par import par
from zython.var_par.array import Array
from zython.operations.constraint.funcs import alldifferent, sum
from zython.operations.constraint.forall import forall
from zython.operations.constraint.exists import exists
from zython.model import Model
from zython.result import as_original

import builtins
builtins.range = zython.var_par.types._range
