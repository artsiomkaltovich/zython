from zython.operations._op_codes import _Op_code


class _Constraint:
    def __init__(self, op, *params, type_=None):
        self.op = op
        self.params = params
        self._type = type_

    @property
    def type(self):
        return self._type

    def __xor__(self, other):
        return _Constraint(_Op_code.xor, self, other)

    def __or__(self, other):
        return _Constraint(_Op_code.or_, self, other)

    def __and__(self, other):
        return _Constraint(_Op_code.and_, self, other)
