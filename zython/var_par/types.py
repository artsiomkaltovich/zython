import zython  # for type hints
from typing import Union, Sequence

from zython.operations.operation import Operation


class _range:
    def __new__(cls, start, stop=None, step=1):
        if stop is None:
            stop = start
            start = 0
        if (isinstance(start, (Operation, float))
                or isinstance(stop, (Operation, float))
                or isinstance(step, (Operation, float))):
            self = super().__new__(cls)
            self.start = start
            self.stop = stop
            self.step = step
            return self
        else:
            return range(start, stop, step)


Ranges = range, _range
RangesType = Union[range, _range]
ZnSequence = Union[RangesType, "zython.var_par.array.ArrayMixin", Sequence["zython.var_par.var.var"]]


def is_range(obj):
    return isinstance(obj, Ranges)


def get_type(arg):
    return getattr(arg, "type", type(arg))
