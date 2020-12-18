from zython.operations.all_ops import Op


class Constraint:
    def __init__(self, op, *params):
        self.op = op
        self.params = params
        self._type = None

    @property
    def type(self):
        return self._type

    def __xor__(self, other):
        return Constraint(Op.xor, self, other)

    def __or__(self, other):
        return Constraint(Op.or_, self, other)

    def __and__(self, other):
        return Constraint(Op.and_, self, other)
