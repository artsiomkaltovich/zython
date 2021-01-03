from zython.operations.all_ops import Op
from zython.operations.constraint.constraint import Constraint


class _Operation(Constraint):
    def __init__(self, op, *params):
        super(_Operation, self).__init__(op, *params)
        if op == Op.size:
            self._type = int

    def __pow__(self, power, modulo=None):
        if modulo is not None:
            raise ValueError("modulo is not supported")
        return _Operation(Op.pow, self, power)

    def __mul__(self, other):
        return _Operation(Op.mul, self, other)

    def __truediv__(self, other):
        return _Operation(Op.truediv, self, other)

    def __floordiv__(self, other):
        return _Operation(Op.floatdiv, self, other)

    def __mod__(self, other):
        return _Operation(Op.mod, self, other)

    def __add__(self, other):
        return _Operation(Op.add, self, other)

    def __sub__(self, other):
        return _Operation(Op.sub, self, other)

    def __eq__(self, other):
        return _Operation(Op.eq, self, other)

    def __ne__(self, other):
        return _Operation(Op.ne, self, other)

    def __lt__(self, other):
        return _Operation(Op.lt, self, other)

    def __gt__(self, other):
        return _Operation(Op.gt, self, other)

    def __le__(self, other):
        return _Operation(Op.le, self, other)

    def __ge__(self, other):
        return _Operation(Op.ge, self, other)
