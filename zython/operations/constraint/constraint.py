class Constraint:
    def __init__(self, op, *params):
        self.op = op
        self.params = params
        self._type = None

    @property
    def type(self):
        return self._type
