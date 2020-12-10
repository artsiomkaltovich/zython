class Constraint:
    def __init__(self, op, *params):
        self.op = op
        self.params = params
        self._str = None

    def __str__(self):
        if self._str is None:
            self._str = self.op(*self.params)
        return self._str

    def __bool__(self):
        raise TypeError("This object is supposed to be used as constraint, not in if or while-clause")


class all_different(Constraint):
    # TODO: array support?
    def __init__(self, *params):
        super().__init__(_all_different, params)


def _all_different(args):
    return f"alldifferent([{', '.join(v.name for v in args)}])"
