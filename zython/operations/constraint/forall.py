from zython.operations.all_ops import Op
from zython.operations.constraint.constraint import Constraint


class forall(Constraint):
    def __init__(self, seq, func):
        super().__init__(Op.forall, seq, func)
