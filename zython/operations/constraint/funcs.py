from zython.operations.all_ops import Op
from zython.operations.constraint.constraint import Constraint


class all_different(Constraint):
    # TODO: array support?
    def __init__(self, *params):
        super().__init__(Op.alldifferent, params)


class sum(Constraint):
    def __init__(self, array, /):
        super().__init__(Op.sum_, array)
        self._type = array.type
