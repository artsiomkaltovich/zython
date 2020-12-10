from zython.operations.constraint import Constraint


class _Operation(Constraint):
    def __init__(self, op, *params):
        super(_Operation, self).__init__(op, *params)

    def __pow__(self, power, modulo=None):
        if modulo is not None:
            raise ValueError("modulo is not supported")
        return _Operation(_pow, self, power)

    def __mul__(self, other):
        return _Operation(_mul, self, other)

    def __truediv__(self, other):
        return _Operation(_truediv, self, other)

    def __floordiv__(self, other):
        return _Operation(_floordiv, self, other)

    def __mod__(self, other):
        return _Operation(_mod, self, other)

    def __add__(self, other):
        return _Operation(_add, self, other)

    def __sub__(self, other):
        return _Operation(_sub, self, other)

    def __eq__(self, other):
        return _Operation(_eq, self, other)

    def __ne__(self, other):
        return _Operation(_ne, self, other)

    def __lt__(self, other):
        return _Operation(_lt, self, other)

    def __gt__(self, other):
        return _Operation(_gt, self, other)

    def __le__(self, other):
        return _Operation(_le, self, other)

    def __ge__(self, other):
        return _Operation(_ge, self, other)

    def __xor__(self, other):
        return _Operation(_xor, self, other)

    def __or__(self, other):
        return _Operation(_or, self, other)

    def __and__(self, other):
        return _Operation(_and, self, other)


def _pow(a, b, /):
    return f"pow({a}, {b})"


def _mul(a, b, /):
    return f"({a} * {b})"


def _truediv(a, b, /):
    return f"({a} / {b})"


def _floordiv(a, b, /):
    return f"({a} div {b})"


def _mod(a, b, /):
    return f"({a} mod {b})"


def _add(a, b, /):
    return f"({a} + {b})"


def _sub(a, b, /):
    return f"({a} - {b})"


def _eq(a, b, /):
    return f"({a} == {b})"


def _ne(a, b, /):
    return f"({a} != {b})"


def _lt(a, b, /):
    return f"({a} < {b})"


def _gt(a, b, /):
    return f"({a} > {b})"


def _le(a, b, /):
    return f"({a} <= {b})"


def _ge(a, b, /):
    return f"({a} >= {b})"


def _xor(a, b, /):
    return f"({a} xor {b})"


def _or(a, b, /):
    return f"({a} \\/ {b})"


def _and(a, b, /):
    return f"({a} /\\ {b})"
