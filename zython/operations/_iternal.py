import inspect
from typing import Union, Callable, Tuple, Optional

from zython import var
from zython.operations._operation import _Operation
from zython.operations._constraint import _Constraint
from zython.var_par import types
from zython.var_par.array import ArrayMixin
from zython.var_par.types import is_range


def _get_variable(seq) -> var:
    if is_range(seq):
        v = var(int)
    elif isinstance(seq, ArrayMixin):
        v = var(seq.type)
    else:
        raise ValueError(f"seq should be range, but {type(seq)} was specified")
    return v


def _extract_func_var_and_op(seq: Union[types._range, types.orig_range, ArrayMixin],
                             func: Union[_Constraint, Callable]) -> Tuple[Optional[var], _Operation]:
    variable = None
    parameters = inspect.signature(func).parameters
    if len(parameters) > 1:
        raise ValueError("only functions and lambdas with one arguments are supported")
    elif len(parameters) == 1:
        variable = _get_variable(seq)
        variable._name, _ = dict(parameters).popitem()
        func_op = func(variable)
    else:
        func_op = func()
    return variable, func_op


def get_iter_var_and_op(seq, func):
    iter_var = None
    op = None
    if callable(func):
        iter_var, op = _extract_func_var_and_op(seq, func)
    return iter_var, op
