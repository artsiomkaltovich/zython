import inspect
from functools import singledispatch
from typing import Union, Callable, Tuple, Optional

from zython import var
from zython.operations.operation import Operation
from zython.operations.constraint import Constraint
from zython.var_par import types
from zython.var_par.array import ArrayMixin
from zython.var_par.types import is_range


@singledispatch
def _get_variable(seq) -> var:
    if is_range(seq):
        return var(int)
    raise ValueError(f"seq should be range, but {type(seq)} was specified")


@_get_variable.register(ArrayMixin)  # TODO: newer versions of python support type evaluation from hints
def _(seq: ArrayMixin):
    return var(seq.type)


@_get_variable.register(list)
@_get_variable.register(tuple)
def _(seq: Union[list, tuple]):
    if seq:
        for s in seq:
            if not isinstance(s, var):
                raise ValueError("Arguments of constraints should be zn.var, but {} was passed".format(type(s)))
        v = var(seq[0].type)
    else:
        raise ValueError("empty sequences are not supported as constraint parameter")
    return v


def _extract_func_var_and_op(seq: Union[types._range, types.orig_range, ArrayMixin],
                             func: Union[Constraint, Callable]) -> Tuple[Optional[var], Operation]:
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
