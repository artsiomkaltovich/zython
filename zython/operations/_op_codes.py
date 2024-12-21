import enum


class _Op_code(enum.Enum):
    add = enum.auto()
    sub = enum.auto()
    eq = enum.auto()
    ne = enum.auto()
    lt = enum.auto()
    gt = enum.auto()
    le = enum.auto()
    ge = enum.auto()
    invert = enum.auto()
    xor = enum.auto()
    and_ = enum.auto()
    or_ = enum.auto()
    mul = enum.auto()
    truediv = enum.auto()
    floordiv = enum.auto()
    mod = enum.auto()
    pow = enum.auto()
    sqrt = enum.auto()
    abs = enum.auto()
    exp = enum.auto()
    ln = enum.auto()
    log = enum.auto()
    log10 = enum.auto()
    log2 = enum.auto()
    forall = enum.auto()  # 3 params: (seq, iter_var=None, func=None)
    exists = enum.auto()
    sum_ = enum.auto()
    product = enum.auto()
    count = enum.auto()
    min_ = enum.auto()
    max_ = enum.auto()
    size = enum.auto()
    in_ = enum.auto()
    alldifferent = enum.auto()
    alldifferent_except_0 = enum.auto()
    alldifferent_except = enum.auto()
    allequal = enum.auto()
    ndistinct = enum.auto()
    circuit = enum.auto()
    increasing = enum.auto()
    strictly_increasing = enum.auto()
    decreasing = enum.auto()
    strictly_decreasing = enum.auto()
    cumulative = enum.auto()
    disjunctive = enum.auto()
    disjunctive_strict = enum.auto()
    table = enum.auto()
