from zython.operations._operation import _Operation

orig_range = range


def is_range(obj):
    return isinstance(obj, range) or isinstance(obj, orig_range)


class _range:
    def __new__(cls, start, stop=None, step=1):
        if stop is None:
            stop = start
            start = 0
        if isinstance(start, _Operation) or isinstance(stop, _Operation) or isinstance(step, _Operation):
            self = super().__new__(cls)
            self.start = start
            self.stop = stop
            self.step = step
            return self
        else:
            return orig_range(start, stop, step)
