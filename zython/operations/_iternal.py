import inspect
from functools import singledispatch
from typing import Union, Callable, Tuple, Optional

from zython import var
from zython.operations.constraint import Constraint
from zython.operations.operation import Operation
from zython.var_par.array import ArrayMixin
from zython.var_par.types import is_range, ZnSequence, get_type


@singledispatch
def _get_variable(seq) -> var:
    if is_range(seq):
        return var(int)
    assert False, f"{type(seq)} isn't supported, please use Sequence or Array here"


@_get_variable.register(ArrayMixin)  # TODO: newer versions of python support type evaluation from hints
def _(seq: ArrayMixin):
    return var(seq.type)


@_get_variable.register(list)
@_get_variable.register(tuple)
def _(seq: Union[list, tuple]):
    if seq:
        v = var(get_type(seq[0]))
    else:
        raise ValueError("empty sequences are not supported as constraint parameter")
    return v


def _extract_func_var_and_op(seq: ZnSequence,
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
    if callable(func):
        iter_var, func = _extract_func_var_and_op(seq, func)
    return iter_var, func
