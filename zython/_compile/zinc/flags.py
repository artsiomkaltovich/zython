import enum
from functools import partial
from typing import Callable, Dict

from zython._compile.zinc.types import SourceCode


class Flags(enum.Flag):
    none = enum.auto()
    alldifferent = enum.auto()
    alldifferent_except_0 = enum.auto()
    alldifferent_except = enum.auto()
    all_equal = enum.auto()
    nvalue = enum.auto()
    circuit = enum.auto()
    increasing = enum.auto()
    strictly_increasing = enum.auto()
    decreasing = enum.auto()
    strictly_decreasing = enum.auto()
    cumulative = enum.auto()
    disjunctive = enum.auto()
    disjunctive_strict = enum.auto()
    table = enum.auto()
    float_used = enum.auto()


def append(src: SourceCode, line: str):
    src.appendleft(line)


FLAG_PROCESSORS: Dict[Flags, Callable[[SourceCode], None]] = {
    Flags.alldifferent: partial(append, line='include "alldifferent.mzn";'),
    Flags.alldifferent_except_0: partial(append, line='include "alldifferent_except_0.mzn";'),
    Flags.alldifferent_except: partial(append, line='include "alldifferent_except.mzn";'),
    Flags.all_equal: partial(append, line='include "all_equal.mzn";'),
    Flags.nvalue: partial(append, line='include "nvalue_fn.mzn";'),
    Flags.circuit: partial(append, line='include "circuit.mzn";'),
    Flags.increasing: partial(append, line='include "increasing.mzn";'),
    Flags.strictly_increasing: partial(append, line='include "strictly_increasing.mzn";'),
    Flags.decreasing: partial(append, line='include "decreasing.mzn";'),
    Flags.strictly_decreasing: partial(append, line='include "strictly_decreasing.mzn";'),
    Flags.cumulative: partial(append, line='include "cumulative.mzn";'),
    Flags.disjunctive: partial(append, line='include "disjunctive.mzn";'),
    Flags.disjunctive_strict: partial(append, line='include "disjunctive_strict.mzn";'),
    Flags.table: partial(append, line='include "table.mzn";'),
    Flags.float_used: lambda x: x,
}
