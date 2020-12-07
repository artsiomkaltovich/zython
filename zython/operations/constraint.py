class Constrain:
    def __init__(self, op, *params):
        self.op = op
        self.params = params
        self._str = None

    def __str__(self):
        if self._str is None:
            self._str = self.op(*self.params)
        return self._str


class all_different(Constrain):
    # TODO: array support?
    def __init__(self, *params):
        super().__init__(_all_different, params)


def _all_different(args):
    return f"alldifferent([{', '.join(v.name for v in args)}])"
