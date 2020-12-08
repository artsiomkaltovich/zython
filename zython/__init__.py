from zython.var_par.var import var
from zython.var_par.array import Array
from .operations.constraint import all_different
from .operations import functions as func
from .model import Model

__builtins__["all"] = func._all
