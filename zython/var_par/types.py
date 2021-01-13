import zython  # for type hints
from typing import Union, Sequence

from zython.operations.operation import Operation

orig_range = range


def is_range(obj):
    return isinstance(obj, range) or isinstance(obj, orig_range)


class _range:
    def __new__(cls, start, stop=None, step=1):
        if stop is None:
            stop = start
            start = 0
        if isinstance(start, Operation) or isinstance(stop, Operation) or isinstance(step, Operation):
            self = super().__new__(cls)
            self.start = start
            self.stop = stop
            self.step = step
            return self
        else:
            return orig_range(start, stop, step)


ZnSequence = Union[_range, orig_range, "zython.var_par.array.ArrayMixin", Sequence["zython.var_par.var.var"]]


def get_type(arg):
    return getattr(arg, "type", type(arg))
