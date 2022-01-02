import enum
from collections import UserDict
from functools import partial

from zython._compile.zinc.types import SourceCode


class Flags(enum.Flag):
    none = enum.auto()
    alldifferent = enum.auto()
    alldifferent_except_0 = enum.auto()
    all_equal = enum.auto()
    nvalue = enum.auto()
    circuit = enum.auto()
    increasing = enum.auto()
    strictly_increasing = enum.auto()
    decreasing = enum.auto()
    strictly_decreasing = enum.auto()
    float_used = enum.auto()


FLAG_TO_SRC_PREFIX = {
    Flags.alldifferent: 'include "alldifferent.mzn";',
    Flags.alldifferent_except_0: 'include "alldifferent_except_0.mzn";',
    Flags.all_equal: 'include "all_equal.mzn";',
    Flags.nvalue: 'include "nvalue_fn.mzn";',
    Flags.circuit: 'include "circuit.mzn";',
    Flags.increasing: 'include "increasing.mzn";',
    Flags.strictly_increasing: 'include "strictly_increasing.mzn";',
    Flags.decreasing: 'include "decreasing.mzn";',
    Flags.strictly_decreasing: 'include "strictly_decreasing.mzn";',
}


def append(src: SourceCode, line: str):
    src.appendleft(line)


class FlagProcessors(UserDict):
    def __init__(self):
        super().__init__()
        self[Flags.float_used] = None

    def __missing__(self, key):
        return partial(append, line=FLAG_TO_SRC_PREFIX[key])
