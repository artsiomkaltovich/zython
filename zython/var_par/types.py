from typing import Union, Sequence

import zython  # for type hints


def _create_range(cls, start, stop, step):
    obj = object.__new__(cls)
    obj.start = start
    obj.stop = stop
    obj.step = step
    return obj


class _range:
    start: Union[int, float, "zython.operations.operation.Operation"]
    stop: Union[int, float, "zython.operations.operation.Operation"]
    step: Union[int, float, "zython.operations.operation.Operation"]  # only 1 supported for now

    def __new__(cls, start, stop=None, step=1):
        if stop is None:
            stop = start
            start = 0
        if isinstance(start, int) and isinstance(stop, int) and isinstance(step, int):
            return range(start, stop, step)
        if isinstance(start, (int, float)) and isinstance(stop, (int, float)) and isinstance(step, (int, float)):
            return _create_range(cls, float(start), float(stop), float(step))
        return _create_range(cls, start, stop, step)


Ranges = range, _range
RangesType = Union[range, _range]
ZnSequence = Union[
    RangesType,
    "zython.var_par.collections.array.ArrayMixin",
    Sequence["zython.var_par.var.var"],
]
