from zython.operations.all_ops import Op
from zython.operations.constraint.constraint import Constraint


class exists(Constraint):
    def __init__(self, seq, func):
        super().__init__(Op.exists, seq, func)
