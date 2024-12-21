from numbers import Number

import zython
from zython.operations._op_codes import _Op_code
from zython.operations.constraint import Constraint
from zython.var_par.get_type import get_wider_type


class Operation(Constraint):
    def __init__(self, op, *params, type_=None):
        super(Operation, self).__init__(op, *params, type_=type_)

    def __pow__(self, power, modulo=None):
        return _pow(self, power, modulo)

    def __mul__(self, other):
        return _mul(self, other)

    def __rmul__(self, other):
        return _mul(other, self)

    # def __truediv__(self, other):
    #     op = _Operation(_Op_code.truediv, self, other)
    #     op._type = get_wider_type(self, other)
    #     return op
    #
    # def __rtruediv__(self, other):
    #     op = _Operation(_Op_code.mul, other, self)
    #     op._type = get_wider_type(self, other)
    #     return op

    def __floordiv__(self, other):
        return _floordiv(self, other)

    def __rfloordiv__(self, other):
        return _floordiv(other, self)

    def __mod__(self, other):
        return _mod(self, other)

    def __rmod__(self, other):
        return _mod(other, self)

    def __add__(self, other):
        return _add(self, other)

    def __radd__(self, other):
        return _add(other, self)

    def __sub__(self, other):
        return _sub(self, other)

    def __rsub__(self, other):
        return _sub(other, self)

    def __eq__(self, other):
        return Operation(_Op_code.eq, self, other, type_=int)

    def __ne__(self, other):
        return Operation(_Op_code.ne, self, other, type_=int)

    def __lt__(self, other):
        return Operation(_Op_code.lt, self, other, type_=int)

    def __gt__(self, other):
        return Operation(_Op_code.gt, self, other, type_=int)

    def __le__(self, other):
        return Operation(_Op_code.le, self, other, type_=int)

    def __ge__(self, other):
        return Operation(_Op_code.ge, self, other, type_=int)


# Methods below are used for validation and control of _Operation creation
# when you create _Operation as Operation(_Op_code.sum, seq, iter_var, func)
# it is easy to forgot the order and number of variables, so it is better to call
# Operation.sum which has param names and type hints


def _add(left, right):
    return Operation(_Op_code.add, left, right, type_=get_wider_type(left, right))


def _sub(left, right):
    return Operation(_Op_code.sub, left, right, type_=get_wider_type(left, right))


def _pow(base, power, modulo=None):
    if modulo is not None:
        raise ValueError("modulo is not supported")
    return Operation(_Op_code.pow, base, power, type_=get_wider_type(base, power))


def _mul(left, right):
    return Operation(_Op_code.mul, left, right, type_=get_wider_type(left, right))


def _floordiv(left, right):
    _validate_div(left, right)
    return Operation(_Op_code.floordiv, left, right, type_=get_wider_type(left, right))


def _mod(left, right):
    _validate_div(left, right)
    return Operation(_Op_code.mod, left, right, type_=get_wider_type(left, right))


def _size(array: "zython.var_par.collections.array.ArrayMixin", dim: int):
    if 0 <= dim < array.ndims():
        return Operation(_Op_code.size, array, dim, type_=int)
    raise ValueError(f"The array has 0..{array.ndims()} dimensions, but {dim} were specified")


def _in(item: int, array: "zython.var_par.collections.abstract._AbstractCollection"):
    return Operation(_Op_code.in_, item, array, type_=bool)


def _validate_div(left, right):
    if isinstance(right, Number) and right == 0 or getattr(right, "value", 1) == 0:
        raise ValueError("right part of expression can't be 0")
