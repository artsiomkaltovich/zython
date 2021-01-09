import zython
from typing import Union, Callable, Optional, Sequence

from zython.operations import _iternal
from zython.operations._op_codes import _Op_code
from zython.operations.constraint import Constraint
from zython.operations.operation import Operation
from zython.var_par.array import ArrayMixin


class alldifferent(Constraint):
    # TODO: array support?
    def __init__(self, *params):
        super().__init__(_Op_code.alldifferent, params)


class circuit(Constraint):
    def __init__(self, array):
        super().__init__(_Op_code.circuit, array)


def exists(seq: Union["zython.var_par.types._range",
                      "zython.var_par.types.orig_range",
                      "zython.var_par.array.ArrayMixin",
                      Sequence[zython.var]],
           func: Optional[Union["Constraint", Callable]] = None) -> Constraint:
    """ Specify constraint which should be true for `at least` one element in ``seq``.

    The method has the same signature as ``forall``.

    See Also
    --------
    forall

    Examples
    --------

    >>> import zython as zn
    >>> class MyModel(zython.Model):
    ...     def __init__(self):
    ...         self.a = zn.var(range(0, 10))
    ...         self.b = zn.var(range(0, 10))
    ...         self.c = zn.var(range(0, 10))
    ...         self.constraints = [zn.exists((self.a, self.b, self.c), lambda elem: elem > 0)]
    >>> model = MyModel()
    >>> result = model.solve_satisfy()
    >>> sorted((result["a"], result["b"], result["c"]))
    [0, 0, 1]
    """
    iter_var, operation = _iternal.get_iter_var_and_op(seq, func)
    return Constraint.exists(seq, iter_var, operation)


def forall(seq: Union["zython.var_par.types._range",
                      "zython.var_par.types.orig_range",
                      "zython.var_par.array.ArrayMixin",
                      Sequence[zython.var]],
           func: Optional[Union["Constraint", Callable]] = None) -> Constraint:
    """
    Takes expression (that is, constraint) or function which return constraint
        and make them a single constraint which should be true for every element in the array.

    Parameters
    ----------
    seq: range, array of var, or sequence (list or tuple) of var
        sequence to apply ``func``
    func: Constraint or Callable
        Constraint every element in seq should satisfy or function which returns such constraint.
        If function or lambda it should be with 0 or 1 arguments only.

    Returns
    -------
    result: Constraint
        resulted constraint

    Examples
    --------

    >>> import zython as zn
    >>> class MyModel(zython.Model):
    ...     def __init__(self):
    ...         self.a = zn.Array(zn.var(int), shape=3)
    ...         self.constraints = [zn.forall(self.a, lambda elem: elem > 0)]
    >>> model = MyModel()
    >>> model.solve_satisfy()
    Solution(a=[1, 1, 1])
    """
    iter_var, operation = _iternal.get_iter_var_and_op(seq, func)
    return Constraint.forall(seq, iter_var, operation)


def sum(seq, func=None):
    iter_var, operation = _iternal.get_iter_var_and_op(seq, func)
    if isinstance(seq, ArrayMixin) and operation is None:
        type_ = seq.type
    else:
        type_ = operation.type
    if type_ is None:
        raise ValueError("Can't derive the type of {} expression".format(func))
    return Operation(_Op_code.sum_, seq, iter_var, operation, type_=type_)
