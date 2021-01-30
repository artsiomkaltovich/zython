from typing import Union, Callable, Optional

from zython.operations import _iternal
from zython.operations import constraint as constraint_module
from zython.operations import operation as operation_module
from zython.operations._op_codes import _Op_code
from zython.operations.constraint import Constraint
from zython.operations.operation import Operation
from zython.var_par.array import ArrayMixin
from zython.var_par.types import ZnSequence


def exists(seq: ZnSequence,
           func: Optional[Union["Constraint", Callable]] = None) -> Constraint:
    """ Specify constraint which should be true for `at least` one element in ``seq``.

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


def forall(seq: ZnSequence,
           func: Optional[Union["Constraint", Callable]] = None) -> Constraint:
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


def sum(seq: ZnSequence,
        func: Optional[Union["Constraint", Callable]] = None) -> Operation:
    """ Calculate the sum of the ``seq`` according with ``func``

    Iterates through elements in seq and calculate their sum, you can modify summarized expressions
    by specifying ``func`` parameter.

    Parameters
    ----------
    seq: range, array of var, or sequence (list or tuple) of var
        sequence to sum up
    func: Operation or Callable, optional
        Operation which will be executed with every element and later sum up. Or function which returns
        such operation.
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
    if isinstance(seq, ArrayMixin) and operation is None:
        type_ = seq.type
    else:
        type_ = operation.type
    if type_ is None:
        raise ValueError("Can't derive the type of {} expression".format(func))
    return operation_module._sum(seq, iter_var, operation, type_=type_)


def count(seq: ZnSequence, value: Union[int, Operation, Callable[[ZnSequence], Operation]]) -> Operation:
    """ Returns the number of occurrences of ``value`` in ``seq``.

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
    >>> class MyModel(zn.Model):
    ...     def __init__(self):
    ...         self.a = zn.Array(zn.var(range(10)), shape=4)
    ...         self.constraints = [zn.forall(range(self.a.size(0)),
    ...                                       lambda i: zn.count(self.a, lambda elem: elem == self.a[i]) == 1)]
    >>> model = MyModel()
    >>> result = model.solve_satisfy()
    >>> Counter(result["a"])
    Counter({3: 1, 2: 1, 1: 1, 0: 1})
    """
    iter_var, operation = _iternal.get_iter_var_and_op(seq, value)
    return operation_module._count(seq, iter_var, operation, type_=int)


def min(seq: ZnSequence, key: Union[Operation, Callable[[ZnSequence], Operation], None] = None) -> Operation:
    """ Finds the smallest object in ``seq``, according to ``key``

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
    return operation_module._min(seq, iter_var, operation, type_=int)


def max(seq: ZnSequence, key: Union[Operation, Callable[[ZnSequence], Operation], None] = None) -> Operation:
    """ Finds the biggest object in ``seq``, according to ``key``

    Parameters
    ----------
    seq: range, array of var, or sequence (list or tuple) of var
        Sequence to find smallest element in
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

    >>> import zython as zn
    >>> class MyModel(zn.Model):
    ...     def __init__(self):
    ...         self.a = zn.Array([[1, 2, 3], [-1, -2, -3]])
    ...         self.m = zn.max(range(self.a.size(0)), lambda row: zn.count(self.a[row, :], lambda elem: elem < 0))
    >>> model = MyModel()
    >>> model.solve_satisfy()
    Solution(m=3)
    """
    iter_var, operation = _iternal.get_iter_var_and_op(seq, key)
    return operation_module._max(seq, iter_var, operation, type_=int)


class alldifferent(Constraint):
    """ requires all the variables appearing in its argument to be different

    Parameters
    ----------
    seq: range, array of var, or sequence (list or tuple) of var
        sequence elements of which should be distinct
    except0: bool, optional
        if set - ``seq`` can contain any amount of 0.

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
    """
    def __init__(self, seq: ZnSequence, except0: Optional[bool] = None):
        if except0:
            super().__init__(_Op_code.alldifferent_except_0, seq)
        else:
            super().__init__(_Op_code.alldifferent, seq)


class allequal(Constraint):
    """ requires all the variables appearing in its argument to be equal

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
    """ returns the number of distinct values in ``seq``.

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
    """ Constrains the elements of ``seq`` to define a circuit where x[i] = j means that j is the successor of i.

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
    """ Requires that the sequence `seq` is in increasing order

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
    """ Requires that the sequence `seq` is in decreasing order

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
