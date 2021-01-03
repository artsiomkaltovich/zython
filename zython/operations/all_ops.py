import enum


class Op(enum.Enum):
    add = enum.auto()
    sub = enum.auto()
    eq = enum.auto()
    ne = enum.auto()
    lt = enum.auto()
    gt = enum.auto()
    le = enum.auto()
    ge = enum.auto()
    xor = enum.auto()
    and_ = enum.auto()
    or_ = enum.auto()
    mul = enum.auto()
    truediv = enum.auto()
    floatdiv = enum.auto()
    mod = enum.auto()
    pow = enum.auto()
    alldifferent = enum.auto()
    forall = enum.auto()
    sum_ = enum.auto()
    size = enum.auto()
