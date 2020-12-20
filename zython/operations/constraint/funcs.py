from zython.operations._operation import _Operation
from zython.operations.all_ops import Op
from zython.operations.constraint.constraint import Constraint


class alldifferent(Constraint):
    # TODO: array support?
    def __init__(self, *params):
        super().__init__(Op.alldifferent, params)


class sum(_Operation):
    def __init__(self, array):  # TODO: make positional only
        super().__init__(Op.sum_, array)
        self._type = array.type
