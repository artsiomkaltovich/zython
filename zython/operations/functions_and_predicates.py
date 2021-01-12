from typing import Union, Callable, Optional

from zython.operations import _iternal
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
    return Constraint.exists(seq, iter_var, operation)


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
    return Constraint.forall(seq, iter_var, operation)


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
    return Operation.sum(seq, iter_var, operation, type_=type_)


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
    return Operation.count(seq, iter_var, operation, type_=int)


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
    return Operation.min(seq, iter_var, operation, type_=int)


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
    return Operation.max(seq, iter_var, operation, type_=int)


class alldifferent(Constraint):
    """ requires all the variables appearing in its argument to be different

    Parameters
    ----------
    seq: range, array of var, or sequence (list or tuple) of var
        sequence which elements of which should be distinct

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
    """
    def __init__(self, seq: ZnSequence):
        super().__init__(_Op_code.alldifferent, seq)


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
