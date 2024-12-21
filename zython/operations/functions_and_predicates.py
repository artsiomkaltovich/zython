from typing import Union, Callable, Optional

import zython
from zython.operations import _iternal
from zython.operations import constraint as constraint_module
from zython.operations._op_codes import _Op_code
from zython.operations.constraint import Constraint
from zython.operations.operation import Operation
from zython.var_par.collections.set import SetVar
from zython.var_par.get_type import get_base_type, derive_operation_type
from zython.var_par.types import ZnSequence
from zython.var_par.var import var


def exists(seq: ZnSequence, func: Optional[Union["Constraint", Callable]] = None) -> Constraint:
    """Specify constraint which should be true for `at least` one element in ``seq``.

    The method has the same signature as ``forall``.

    See Also
    --------
    forall

    Examples
    --------

    >>> import zython as zn
    >>> class MyModel(zn.Model):
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
    return constraint_module._exists(seq, iter_var, operation)


def forall(seq: ZnSequence, func: Optional[Union["Constraint", Callable]] = None) -> Constraint:
    """
    Takes expression (that is, constraint) or function which return constraint
        and make them a single constraint which should be true for every element in the array.

    Parameters
    ----------
    seq: range, array of var, or sequence (list or tuple) of var
        sequence to apply ``func``
    func: Constraint or Callable, optional
        Constraint every element in seq should satisfy or function which returns such constraint.
        If function or lambda it should be with 0 or 1 arguments only.

    Returns
    -------
    result: Constraint
        resulted constraint

    Examples
    --------

    >>> import zython as zn
    >>> class MyModel(zn.Model):
    ...     def __init__(self):
    ...         self.a = zn.Array(zn.var(int), shape=3)
    ...         self.constraints = [zn.forall(self.a, lambda elem: elem > 0)]
    >>> model = MyModel()
    >>> model.solve_satisfy()
    Solution(a=[1, 1, 1])
    """
    iter_var, operation = _iternal.get_iter_var_and_op(seq, func)
    return constraint_module._forall(seq, iter_var, operation)


def sum(seq: ZnSequence, func: Optional[Union["Constraint", Callable]] = None) -> Operation:
    """Calculate the sum of the ``seq`` according with ``func``

    Iterates through elements in seq and calculate their sum, you can modify summarized expressions
    by specifying ``func`` parameter.

    Parameters
    ----------
    seq: range, array of var, or sequence (list or tuple) of var
        sequence to sum up
    func: Operation or Callable, optional
        Operation which will be executed with every element and later sum up. 
        Or function which returns such operation.
        If function or lambda it should be with 0 or 1 arguments only.

    Returns
    -------
    result: Operation
        Operation which will calculate the sum

    Examples
    --------

    >>> import zython as zn
    >>> class MyModel(zn.Model):
    ...     def __init__(self):
    ...         self.a = zn.Array(zn.var(range(1, 10)), shape=4)
    >>> model = MyModel()
    >>> model.solve_minimize(zn.sum(model.a))
    Solution(objective=4, a=[1, 1, 1, 1])

    # find minimal integer sides of the right triangle

    >>> import zython as zn
    >>> class MyModel(zn.Model):
    ...     def __init__(self):
    ...         self.a = zn.var(int)
    ...         self.b = zn.var(int)
    ...         self.c = zn.var(int)
    ...         self.constraints = [self.c ** 2 == zn.sum((self.a, self.b), lambda i: i ** 2),
    ...                             zn.forall((self.a, self.b, self.c), lambda i: i > 0)]
    >>> model = MyModel()
    >>> model.solve_minimize(model.c)
    Solution(objective=5, a=4, b=3, c=5)
    """
    iter_var, operation = _iternal.get_iter_var_and_op(seq, func)
    type_ = derive_operation_type(seq, operation)
    return Operation(_Op_code.sum_, seq, iter_var, operation, type_=type_)

def product(seq: ZnSequence, func: Optional[Union["Constraint", Callable]] = None) -> Operation:
    """Calculate the product of the ``seq`` according to ``func``

    Iterates through elements in seq and calculates their product, you can modify the expressions
    being multiplied by specifying the ``func`` parameter.

    Parameters
    ----------
    seq: range, array of var, or sequence (list or tuple) of var
        sequence to multiply
    func: Operation or Callable, optional
        Operation which will be executed with every element and later multiplied.
        Or function which returns such operation.
        If function or lambda it should be with 0 or 1 arguments only.

    Returns
    -------
    result: Operation
        Operation which will calculate the product

    Examples
    --------

    >>> import zython as zn
    >>> class MyModel(zn.Model):
    ...     def __init__(self):
    ...         self.a = zn.Array(zn.var(range(1, 5)), shape=4)
    >>> model = MyModel()
    >>> model.solve_minimize(zn.product(model.a))
    Solution(objective=1, a=[1, 1, 1, 1])

    # find the product of squares of elements

    >>> import zython as zn
    >>> class MyModel(zn.Model):
    ...     def __init__(self):
    ...         self.a = zn.var(zn.range(4))
    ...         self.b = zn.var(zn.range(4))
    ...         self.c = zn.var(zn.range(4))
    ...         self.constraints = [zn.product((self.a, self.b, self.c), lambda i: i ** 2) == 36]
    >>> model = MyModel()
    >>> model.solve_satisfy()
    Solution(a=3, b=2, c=1)
    """
    iter_var, operation = _iternal.get_iter_var_and_op(seq, func)
    type_ = derive_operation_type(seq, operation)
    return Operation(_Op_code.product, seq, iter_var, operation, type_=type_)


def count(seq: ZnSequence, value: Union[int, Operation, Callable[[ZnSequence], Operation]]) -> Operation:
    """Returns the number of occurrences of ``value`` in ``seq``.

    Parameters
    ----------
    seq: range, array of var, or sequence (list or tuple) of var
        Sequence to count ``value`` in
    value: Operation or Callable, optional
        Operation or constant which will be counted in ``seq``. Or function which returns such value.
        If function or lambda it should be with 0 or 1 arguments only.

    Returns
    -------
    result: Operation
        Operation which will calculate the number of ``value`` in ``seq``.

    Examples
    --------

    Simple timeshedule problem: you with your neighbor wanted to deside who will wash the dishes in the next week.
    You should do it 3 days (because you've bought fancy doormat) and your neighbour - 4 days.

    >>> from collections import Counter
    >>> import zython as zn
    >>> class MyModel(zn.Model):
    ...     def __init__(self):
    ...         self.a = zn.Array(zn.var(range(2)), shape=7)
    ...         self.constraints = [zn.count(self.a, 0) == 3, zn.count(self.a, 1) == 4]
    >>> model = MyModel()
    >>> result = model.solve_satisfy()
    >>> Counter(result["a"])
    Counter({1: 4, 0: 3})

    ``zn.alldifferent`` could be emulated via ``zn.count``

    >>> import zython as zn
    >>> def all_different(array):
    ...     return zn.forall(array, lambda elem: zn.count(array, elem) == 1)
    ...
    >>> class MyModel(zn.Model):
    ...     def __init__(self):
    ...         self.a = zn.Array(zn.var(range(4)), shape=4)
    ...         self.constraints = [all_different(self.a)]
    ...
    >>> model = MyModel()
    >>> result = model.solve_satisfy()
    >>> Counter(result["a"])
    Counter({3: 1, 2: 1, 1: 1, 0: 1})
    """
    iter_var, operation = _iternal.get_iter_var_and_op(seq, value)
    return Operation(_Op_code.count, seq, iter_var, operation, type_=int)


def cumulative(
    start_times: ZnSequence,
    durations: ZnSequence,
    requirements: ZnSequence,
    limit: Union[int, var],
) -> Constraint:
    """The cumulative constraint is used for describing cumulative resource usage.

    It requires that a set of tasks given by start times, durations, and resource requirements,
    never require more than a global resource limit at any one time.

    Parameters
    ----------
    start_times: range, array of var, or sequence (list or tuple) of var
        Sequence with start time of the tasks
    durations: range, array of var, or sequence (list or tuple) of var
        Sequence with durations of the tasks
    requirements: range, array of var, or sequence (list or tuple) of var
        Sequence with resource requirements of the tasks
    limit: int
        Resource limit, which shouldn't be exceeded

    Returns
    -------
    result: Constraint

    Notes
    -----
    It is suggested to use ranges and sequences of ranges instead of int,
    because minizinc can return strange result when type of any arg is int

    Examples
    --------

    How many waiters is necessary to serve all table without delays.
    It is expected, only one waiter will serve any table.

    >>> import zython as zn
    >>> class MyModel(zn.Model):
    ...     def __init__(self):
    ...         self.limit = zn.var(range(0, 10))
    ...         self.constraints = [
    ...             zn.cumulative(start_times=[1, 2, 4],
    ...                           durations=[3, 2, 1],
    ...                           requirements=[1, 1, 1],
    ...                           limit=self.limit,
    ...             ),
    ...         ]
    ...
    >>> model = MyModel()
    >>> result = model.solve_minimize(model.limit)
    >>> result["limit"]
    2
    """
    return Constraint(_Op_code.cumulative, start_times, durations, requirements, limit)


def disjunctive(
    start_times: ZnSequence,
    durations: ZnSequence,
    strict: bool = False,
) -> Constraint:
    """The disjunctive constraint takes an array of start times for each task and
    an array of their durations and makes sure that only one task is active at any one time.

    Parameters
    ----------
    start_times: range, array of var, or sequence (list or tuple) of var
        Sequence with start time of the tasks
    durations: range, array of var, or sequence (list or tuple) of var
        Sequence with durations of the tasks
    strict: bool
        Run in strict mode, which add the following restriction:
        Tasks with a duration of 0 CANNOT be scheduled at any time but only when no other task is running.

    Returns
    -------
    result: Constraint

    Notes
    -----
    It is suggested to use ranges and sequences of ranges instead of int,
    because minizinc can return strange result when type of any arg is int

    Examples
    --------

    >>> import zython as zn
    >>> class MyModel(zn.Model):
    ...     def __init__(self):
    ...         self.start = zn.Array(zn.var(zn.range(0, 10)), shape=3)
    ...         self.constraints = [
    ...             zn.disjunctive(start_times=self.start, durations=[3, 2, 1]),
    ...         ]
    ...
    >>> model = MyModel()
    >>> result = model.solve_satisfy()
    >>> result["start"]
    [3, 1, 0]
    """
    if strict:
        return Constraint(_Op_code.disjunctive_strict, start_times, durations)
    return Constraint(_Op_code.disjunctive, start_times, durations)


def table(
    x: ZnSequence,
    t: ZnSequence,
) -> Constraint:
    """The table constraint is used to specify if one dimensional array
        should be equal to any row of a two-dimensional array.

    Or, in more strict form:
    the table constraint enforces that a tuple of variables takes a value from a set of tuples.
    Since there are no tuples in MiniZinc this is encoded using arrays.
    The constraint enforces x in t, where we consider x and each row in t to be a tuple,
        and t to be a set of tuples.

    Parameters
    ----------
    x: one-dimentional array
    t: two-dimentional array, `x` should be one of the rows of `t`

    Examples
    --------

    >>> import zython as zn
    >>> class MyModel(zn.Model):
    ...     def __init__(self):
    ...         self.a = zn.Array(zn.var(zn.range(1, 5)), shape=4)
    ...         self.choose_from = zn.Array([[1, 2, 3, 4], [0, 1, 2, 3]])
    ...         self.constraints = [zn.table(self.a, self.choose_from)]
    ...
    >>> model = MyModel()
    >>> result = model.solve_satisfy()
    >>> result["a"]
    [1, 2, 3, 4]
    """
    return Constraint(_Op_code.table, x, t)


def abs(x: Union[float, var]) -> Operation:
    """Return absolute value of x

    Returns
    -------
    result: Operation
        Operation which will find the abs.

    Examples
    --------

    >>> import zython as zn
    >>> class MyModel(zn.Model):
    ...     def __init__(self):
    ...         self.a = zn.abs(-1)
    ...         self.p = zn.par(1)
    ...         self.v = zn.var(float)
    ...         self.b = zn.abs(self.p)
    ...         self.c = zn.abs(self.v)
    ...         self.constraints = [self.v == zn.abs(-3)]
    >>> model = MyModel()
    >>> model.solve_satisfy()
    Solution(a=1, v=3.0, b=1, c=3.0)
    """
    return Operation(_Op_code.abs, x, type_=get_base_type(x))

def exp(x: Union[float, var]) -> Operation:
    """Return the exponential of x

    Returns
    -------
    result: Operation
        Operation which will calculate the exponential.

    Examples
    --------

    >>> import zython as zn
    >>> class MyModel(zn.Model):
    ...     def __init__(self):
    ...         self.a = zn.exp(1)
    ...         self.b = zn.var(float)
    ...         self.constraints = [self.b == zn.exp(2)]
    >>> model = MyModel()
    >>> model.solve_satisfy()
    Solution(a=2.718281828459045, b=7.38905609893065)
    """
    return Operation(_Op_code.exp, x, type_=float)

def ln(x: Union[float, var]) -> Operation:
    """Return the natural logarithm of x

    Returns
    -------
    result: Operation
        Operation which will calculate the natural logarithm.

    Examples
    --------

    >>> import zython as zn
    >>> class MyModel(zn.Model):
    ...     def __init__(self):
    ...         self.a = zn.ln(7.38905609893065)
    ...         self.b = zn.var(float)
    ...         self.constraints = [self.b == zn.ln(2.718281828459045)]
    >>> model = MyModel()
    >>> model.solve_satisfy()
    Solution(a=2.0, b=1.0)
    """
    return Operation(_Op_code.ln, x, type_=float)

def log(x: Union[float, var], base: float) -> Operation:
    """Return the logarithm of x to the given base

    Returns
    -------
    result: Operation
        Operation which will calculate the logarithm.

    Examples
    --------

    >>> import zython as zn
    >>> class MyModel(zn.Model):
    ...     def __init__(self):
    ...         self.a = zn.log(8, 2)
    ...         self.b = zn.var(float)
    ...         self.constraints = [self.b == zn.log(27, 3)]
    >>> model = MyModel()
    >>> model.solve_satisfy()
    Solution(a=3.0, b=3.0)
    """
    return Operation(_Op_code.log, base, x, type_=float)

def log10(x: Union[float, var]) -> Operation:
    """Return the base-10 logarithm of x

    Returns
    -------
    result: Operation
        Operation which will calculate the base-10 logarithm.

    Examples
    --------

    >>> import zython as zn
    >>> class MyModel(zn.Model):
    ...     def __init__(self):
    ...         self.a = zn.log10(100)
    ...         self.b = zn.var(float)
    ...         self.constraints = [self.b == zn.log10(1000)]
    >>> model = MyModel()
    >>> model.solve_satisfy()
    Solution(a=2.0, b=3.0)
    """
    return Operation(_Op_code.log10, x, type_=float)

def log2(x: Union[float, var]) -> Operation:
    """Return the base-2 logarithm of x

    Returns
    -------
    result: Operation
        Operation which will calculate the base-2 logarithm.

    Examples
    --------

    >>> import zython as zn
    >>> class MyModel(zn.Model):
    ...     def __init__(self):
    ...         self.a = zn.log2(8)
    ...         self.b = zn.var(float)
    ...         self.constraints = [self.b == zn.log2(16)]
    >>> model = MyModel()
    >>> model.solve_satisfy()
    Solution(a=3.0, b=4.0)
    """
    return Operation(_Op_code.log2, x, type_=float)

def sqrt(x: Union[float, var]) -> Operation:
    """Return the square root of x

    Returns
    -------
    result: Operation
        Operation which will calculate the square root.

    Examples
    --------

    >>> import zython as zn
    >>> class MyModel(zn.Model):
    ...     def __init__(self):
    ...         self.a = zn.sqrt(4)
    ...         self.b = zn.var(float)
    ...         self.constraints = [self.b == zn.sqrt(9)]
    >>> model = MyModel()
    >>> model.solve_satisfy()
    Solution(a=2.0, b=3.0)
    """
    return Operation(_Op_code.sqrt, x, type_=float)

def acos(x: Union[float, var]) -> Operation:
    """Return the arc cosine of x

    Returns
    -------
    result: Operation
        Operation which will calculate the arc cosine.

    Examples
    --------

    >>> import zython as zn
    >>> class MyModel(zn.Model):
    ...     def __init__(self):
    ...         self.a = zn.acos(1)
    ...         self.b = zn.var(float)
    ...         self.constraints = [self.b == zn.acos(0)]
    >>> model = MyModel()
    >>> model.solve_satisfy()
    Solution(a=0.0, b=1.570796326794897)
    """
    return Operation(_Op_code.acos, x, type_=float)

# def acosh(x: Union[float, var]) -> Operation:
#     """Return the inverse hyperbolic cosine of x
# 
#     Returns
#     -------
#     result: Operation
#         Operation which will calculate the inverse hyperbolic cosine.
# 
#     Examples
#     --------
# 
#     >>> import zython as zn
#     >>> class MyModel(zn.Model):
#     ...     def __init__(self):
#     ...         self.a = zn.acosh(1)
#     ...         self.b = zn.var(float)
#     ...         self.constraints = [self.b == zn.acosh(2)]
#     >>> model = MyModel()
#     >>> model.solve_satisfy()
#     Solution(a=0.0, b=1.316957896924817)
#     """
#     return Operation(_Op_code.acosh, x, type_=float)

def asin(x: Union[float, var]) -> Operation:
    """Return the arc sine of x

    Returns
    -------
    result: Operation
        Operation which will calculate the arc sine.

    Examples
    --------

    >>> import zython as zn
    >>> class MyModel(zn.Model):
    ...     def __init__(self):
    ...         self.a = zn.asin(0)
    ...         self.b = zn.var(float)
    ...         self.constraints = [self.b == zn.asin(1)]
    >>> model = MyModel()
    >>> model.solve_satisfy()
    Solution(a=0.0, b=1.570796326794897)
    """
    return Operation(_Op_code.asin, x, type_=float)

# def asinh(x: Union[float, var]) -> Operation:
#     """Return the inverse hyperbolic sine of x
# 
#     Returns
#     -------
#     result: Operation
#         Operation which will calculate the inverse hyperbolic sine.
# 
#     Examples
#     --------
# 
#     >>> import zython as zn
#     >>> class MyModel(zn.Model):
#     ...     def __init__(self):
#     ...         self.a = zn.asinh(0)
#     ...         self.b = zn.var(float)
#     ...         self.constraints = [self.b == zn.asinh(1)]
#     >>> model = MyModel()
#     >>> model.solve_satisfy()
#     Solution(a=0.0, b=0.881373587019543)
#     """
#     return Operation(_Op_code.asinh, x, type_=float)

def atan(x: Union[float, var]) -> Operation:
    """Return the arc tangent of x

    Returns
    -------
    result: Operation
        Operation which will calculate the arc tangent.

    Examples
    --------

    >>> import zython as zn
    >>> class MyModel(zn.Model):
    ...     def __init__(self):
    ...         self.a = zn.atan(0)
    ...         self.b = zn.var(float)
    ...         self.constraints = [self.b == zn.atan(1)]
    >>> model = MyModel()
    >>> model.solve_satisfy()
    Solution(a=0.0, b=0.7853981633974483)
    """
    return Operation(_Op_code.atan, x, type_=float)

#def atanh(x: Union[float, var]) -> Operation:
#    """Return the inverse hyperbolic tangent of x
#
#    Returns
#    -------
#    result: Operation
#        Operation which will calculate the inverse hyperbolic tangent.
#
#    Examples
#    --------
#
#    >>> import zython as zn
#    >>> class MyModel(zn.Model):
#    ...     def __init__(self):
#    ...         self.a = zn.atanh(0)
#    ...         self.b = zn.var(float)
#    ...         self.constraints = [self.b == zn.atanh(0.99)]
#    >>> model = MyModel()
#    >>> model.solve_satisfy()
#    Solution(a=0.0, b=2.646652412362246)
#    """
#    return Operation(_Op_code.atanh, x, type_=float)

def cos(x: Union[float, var]) -> Operation:
    """Return the cosine of x

    Returns
    -------
    result: Operation
        Operation which will calculate the cosine.

    Examples
    --------

    >>> import zython as zn
    >>> class MyModel(zn.Model):
    ...     def __init__(self):
    ...         self.a = zn.cos(0)
    ...         self.b = zn.var(float)
    ...         self.constraints = [self.b == zn.cos(3.141592653589793)]
    >>> model = MyModel()
    >>> model.solve_satisfy()
    Solution(a=1.0, b=-1.0)
    """
    return Operation(_Op_code.cos, x, type_=float)

# def cosh(x: Union[float, var]) -> Operation:
#     """Return the hyperbolic cosine of x
# 
#     Returns
#     -------
#     result: Operation
#         Operation which will calculate the hyperbolic cosine.
# 
#     Examples
#     --------
# 
#     >>> import zython as zn
#     >>> class MyModel(zn.Model):
#     ...     def __init__(self):
#     ...         self.a = zn.cosh(0)
#     ...         self.b = zn.var(float)
#     ...         self.constraints = [self.b == zn.cosh(1)]
#     >>> model = MyModel()
#     >>> model.solve_satisfy()
#     Solution(a=1.0, b=1.543080634815244)
#     """
#     return Operation(_Op_code.cosh, x, type_=float)

def sin(x: Union[float, var]) -> Operation:
    """Return the sine of x

    Returns
    -------
    result: Operation
        Operation which will calculate the sine.

    Examples
    --------

    >>> import zython as zn
    >>> class MyModel(zn.Model):
    ...     def __init__(self):
    ...         self.a = zn.sin(0)
    ...         self.b = zn.var(float)
    ...         self.constraints = [self.b == zn.sin(3.141592653589793 / 2)]
    >>> model = MyModel()
    >>> model.solve_satisfy()
    Solution(a=0.0, b=1.0)
    """
    return Operation(_Op_code.sin, x, type_=float)

# def sinh(x: Union[float, var]) -> Operation:
#     """Return the hyperbolic sine of x
# 
#     Returns
#     -------
#     result: Operation
#         Operation which will calculate the hyperbolic sine.
# 
#     Examples
#     --------
# 
#     >>> import zython as zn
#     >>> class MyModel(zn.Model):
#     ...     def __init__(self):
#     ...         self.a = zn.sinh(0)
#     ...         self.b = zn.var(float)
#     ...         self.constraints = [self.b == zn.sinh(1)]
#     >>> model = MyModel()
#     >>> model.solve_satisfy()
#     Solution(a=0.0, b=1.175201193643801)
#     """
#     return Operation(_Op_code.sinh, x, type_=float)

def tan(x: Union[float, var]) -> Operation:
    """Return the tangent of x

    Returns
    -------
    result: Operation
        Operation which will calculate the tangent.

    Examples
    --------

    >>> import zython as zn
    >>> class MyModel(zn.Model):
    ...     def __init__(self):
    ...         self.a = zn.tan(0)
    ...         self.b = zn.var(float)
    ...         self.constraints = [self.b == zn.tan(0.7853981633974484)]
    >>> model = MyModel()
    >>> model.solve_satisfy()
    Solution(a=0.0, b=1.0)
    """
    return Operation(_Op_code.tan, x, type_=float)

# def tanh(x: Union[float, var]) -> Operation:
#     """Return the hyperbolic tangent of x
# 
#     Returns
#     -------
#     result: Operation
#         Operation which will calculate the hyperbolic tangent.
# 
#     Examples
#     --------
# 
#     >>> import zython as zn
#     >>> class MyModel(zn.Model):
#     ...     def __init__(self):
#     ...         self.a = zn.tanh(0)
#     ...         self.b = zn.var(float)
#     ...         self.constraints = [self.b == zn.tanh(1)]
#     >>> model = MyModel()
#     >>> model.solve_satisfy()
#     Solution(a=0.0, b=0.7615941559557649)
#     """
#     return Operation(_Op_code.tanh, x, type_=float)

def min(seq: ZnSequence, key: Union[Operation, Callable[[ZnSequence], Operation], None] = None) -> Operation:
    """Finds the smallest object in ``seq``, according to ``key``

    Parameters
    ----------
    seq: range, array of var, or sequence (list or tuple) of var
        Sequence to find smallest element in
    key: Operation or Callable, optional
        The parameter has the same semantic as in python: specify the operation which result will be latter compared.

    Returns
    -------
    result: Operation
        Operation which will find the smallest element.

    See Also
    --------
    max

    Examples
    --------

    >>> import zython as zn
    >>> class MyModel(zn.Model):
    ...     def __init__(self):
    ...         self.a = zn.Array([[1, 2, 3], [-1, -2, -3]])
    ...         self.m = zn.min(self.a)
    >>> model = MyModel()
    >>> model.solve_satisfy()
    Solution(m=-3)
    """
    iter_var, operation = _iternal.get_iter_var_and_op(seq, key)
    type_ = derive_operation_type(seq, operation)
    return Operation(_Op_code.min_, seq, iter_var, operation, type_=type_)


def max(seq: ZnSequence, key: Union[Operation, Callable[[ZnSequence], Operation], None] = None) -> Operation:
    """Finds the biggest object in ``seq``, according to ``key``

    Parameters
    ----------
    seq: range, array of var, or sequence (list or tuple) of var
        Sequence to find the biggest element in
    key: Operation or Callable, optional
        The parameter has the same semantic as in python: specify the operation which result will be latter compared.

    Returns
    -------
    result: Operation
        Operation which will find the biggest element.

    See Also
    --------
    min

    Examples
    --------

    Calculate the biggest number of negative numbers in a row of an array

    >>> import zython as zn
    >>> class MyModel(zn.Model):
    ...     def __init__(self):
    ...         self.a = zn.Array([[0, 0, 0, 0], [0, 0, -1, -1], [0, -1, -1, -1]])
    ...         self.m = zn.max(zn.range(self.a.size(0)),
    ...                         lambda row: zn.count(self.a[row, :], lambda elem: elem < 0))
    >>> model = MyModel()
    >>> model.solve_satisfy()
    Solution(m=3)
    """
    iter_var, operation = _iternal.get_iter_var_and_op(seq, key)
    type_ = derive_operation_type(seq, operation)
    return Operation(_Op_code.max_, seq, iter_var, operation, type_=type_)


class alldifferent(Constraint):
    """Requires all the variables appearing in its argument to be different

    Parameters
    ----------
    seq: range, array of var, or sequence (list or tuple) of var
        sequence elements of which should be distinct
    except0: bool, optional
        if set - ``seq`` can contain any amount of 0.
    except_: set, zn.Set
        if set - ``seq`` can contain any amount of provided values.

    See Also
    --------
    allequal
    ndistinct

    Examples
    --------

    >>> import zython as zn
    >>> class MyModel(zn.Model):
    ...     def __init__(self):
    ...         self.a = zn.Array(zn.var(range(1, 10)), shape=5)
    ...         self.x = zn.var(range(3))
    ...         self.y = zn.var(range(3))
    ...         self.z = zn.var(range(3))
    ...         self.constraints = [zn.alldifferent(self.a[:3]), zn.alldifferent((self.x, self.y, self.z))]
    >>> model = MyModel()
    >>> model.solve_satisfy()
    Solution(a=[3, 2, 1, 1, 1], x=2, y=1, z=0)

    If ``except0`` flag is set constraint doesn't affect 0'es in the ``seq``

    >>> from collections import Counter
    >>> import zython as zn
    >>> class MyModel(zn.Model):
    ...     def __init__(self):
    ...         self.a = zn.Array(zn.var(range(5)), shape=6)
    ...         self.constraints = [zn.alldifferent(self.a, except0=True), zn.sum(self.a) == 10]
    >>> model = MyModel()
    >>> result = model.solve_satisfy()
    >>> Counter(result["a"]) == {0: 2, 4: 1, 3: 1, 2: 1, 1: 1}
    True

    If ``except_`` flag is set, any amounts of values, specified can be presented in the collection

    >>> from collections import Counter
    >>> import zython as zn
    >>> class MyModel(zn.Model):
    ...     def __init__(self):
    ...         self.a = zn.Array(zn.var(range(1, 4)), shape=4)
    ...         self.constraints = [zn.alldifferent(self.a, except_={1,}), zn.sum(self.a) == 7]
    >>> model = MyModel()
    >>> result = model.solve_satisfy()
    >>> Counter(result["a"]) == {3: 1, 2: 1, 1: 2}
    True
    """

    def __init__(
        self,
        seq: ZnSequence,
        except0: Optional[bool] = None,
        except_: Union[set, zython.var_par.collections.set.Set, None] = None,
    ):
        if all((except0, except_)):
            raise ValueError("Arguments `except0` and `except_` can't be set at the same time")
        if except0:
            super().__init__(_Op_code.alldifferent_except_0, seq)
        elif except_:
            if isinstance(except_, SetVar):
                raise ValueError("Minizinc doesn't support set of var as `except_` argument")
            super().__init__(_Op_code.alldifferent_except, seq, except_)
        else:
            super().__init__(_Op_code.alldifferent, seq)


class allequal(Constraint):
    """Requires all the variables appearing in its argument to be equal

    Parameters
    ----------
    seq: range, array of var, or sequence (list or tuple) of var
        sequence elements of which should be distinct

    See Also
    --------
    alldifferent
    ndistinct

    Examples
    --------

    >>> import zython as zn
    >>> class MyModel(zn.Model):
    ...     def __init__(self):
    ...         self.a = zn.Array(zn.var(range(1, 10)), shape=(2, 4))
    ...         self.constraints = [self.a[0, 0] == 5, zn.allequal(self.a)]
    >>> model = MyModel()
    >>> model.solve_satisfy()
    Solution(a=[[5, 5, 5, 5], [5, 5, 5, 5]])
    """

    def __init__(self, seq: ZnSequence):
        super().__init__(_Op_code.allequal, seq)


class ndistinct(Operation):
    """Returns the number of distinct values in ``seq``.

    Parameters
    ----------
    seq: range, array of var, or sequence (list or tuple) of var
        sequence elements of which should be distinct

    See Also
    --------
    alldifferent
    ndistinct

    Returns
    -------
    n: Operation
        Operation, which calculates the number of distinct values in ``seq``

    Examples
    --------

    >>> import zython as zn
    >>> class MyModel(zn.Model):
    ...     def __init__(self, n):
    ...         self.a = zn.Array(zn.var(range(1, 10)), shape=5)
    ...         self.constraints = [zn.ndistinct(self.a) == n]
    >>> model = MyModel(3)
    >>> result = model.solve_satisfy()
    >>> len(set(result["a"]))
    3
    """

    def __init__(self, seq: ZnSequence):
        super().__init__(_Op_code.ndistinct, seq)


class circuit(Constraint):
    """Constrains the elements of ``seq`` to define a circuit where x[i] = j means that j is the successor of i.

    Examples
    --------

    >>> import zython as zn
    >>> class MyModel(zn.Model):
    ...     def __init__(self):
    ...         self.a = zn.Array(zn.var(range(5)), shape=5)
    ...         self.constraints = [zn.circuit(self.a)]
    >>> model = MyModel()
    >>> model.solve_satisfy()
    Solution(a=[2, 4, 3, 1, 0])
    """

    def __init__(self, seq: ZnSequence):
        super().__init__(_Op_code.circuit, seq)


def increasing(seq: ZnSequence, *, allow_duplicate: Optional[bool] = True) -> Constraint:
    """Requires that the sequence `seq` is in increasing order

    Parameters
    ----------
    seq: range, array of var, or sequence (list or tuple) of var
        sequence elements of which should be increasing
    allow_duplicate: bool, optional
        If `True` duplicates in the array are allowed

    See Also
    --------
    decreasing
    arg_sort

    Examples
    --------

    >>> import zython as zn
    >>> class MyModel(zn.Model):
    ...     def __init__(self):
    ...         self.a = zn.Array(zn.var(range(3)), shape=3)
    ...         self.b = zn.Array(zn.var(range(3)), shape=3)
    ...         self.constraints = [zn.increasing(self.a), zn.increasing(self.b, allow_duplicate=False)]
    >>> model = MyModel()
    >>> model.solve_satisfy()
    Solution(a=[0, 0, 0], b=[0, 1, 2])
    """
    if allow_duplicate:
        return Constraint(_Op_code.increasing, seq)
    else:
        return Constraint(_Op_code.strictly_increasing, seq)


def decreasing(seq: ZnSequence, *, allow_duplicate: Optional[bool] = True) -> Constraint:
    """Requires that the sequence `seq` is in decreasing order

    Parameters
    ----------
    seq: range, array of var, or sequence (list or tuple) of var
        sequence elements of which should be decreasing
    allow_duplicate: bool, optional
        If `True` duplicates in the array are allowed

    See Also
    --------
    increasing
    arg_sort

    Examples
    --------

    >>> import zython as zn
    >>> class MyModel(zn.Model):
    ...     def __init__(self):
    ...         self.a = zn.Array(zn.var(range(3)), shape=3)
    ...         self.b = zn.Array(zn.var(range(3)), shape=3)
    ...         self.constraints = [zn.decreasing(self.a), zn.decreasing(self.b, allow_duplicate=False)]
    >>> model = MyModel()
    >>> model.solve_satisfy()
    Solution(a=[0, 0, 0], b=[2, 1, 0])
    """
    if allow_duplicate:
        return Constraint(_Op_code.decreasing, seq)
    else:
        return Constraint(_Op_code.strictly_decreasing, seq)
