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


class all_different(Constraint):
    # TODO: array support?
    def __init__(self, *params):
        super().__init__(_all_different, params)


def _all_different(args):
    return f"alldifferent([{', '.join(v.name for v in args)}])"


class sum(Constraint):
    def __init__(self, array, /):
        super().__init__(_sum, array)
        self._type = array.type


def _sum(arg, /):
    #return f"sum(i__ in 0..{len(arg)})({arg.name}[i__])"
    return f"sum({arg.name})"
