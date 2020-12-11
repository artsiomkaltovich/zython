class Constraint:
    def __init__(self, op, *params):
        self.op = op
        self.params = params
        self._str = None
        self._type = None

    def __str__(self):
        if self._str is None:
            self._str = self.op(*self.params)
        return self._str

    @property
    def type(self):
        return self._type
