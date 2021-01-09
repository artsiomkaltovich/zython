import zython
from typing import Union, Optional, Callable, Sequence

from zython.operations._op_codes import _Op_code


class Constraint:
    def __init__(self, op, *params, type_=None):
        self.op = op
        self.params = params
        self._type = type_

    @property
    def type(self):
        return self._type

    def __invert__(self):
        return Constraint(_Op_code.invert, self)

    def __xor__(self, other):
        return Constraint(_Op_code.xor, self, other)

    def __or__(self, other):
        return Constraint(_Op_code.or_, self, other)

    def __and__(self, other):
        return Constraint(_Op_code.and_, self, other)

    @staticmethod
    def exists(seq: Union["zython.var_par.types._range",
                          "zython.var_par.types.orig_range",
                          "zython.var_par.array.ArrayMixin",
                          Sequence["zython.var"]],
               iter_var: Optional["zython.var"] = None,
               func: Optional[Union["Constraint", Callable]] = None) -> "Constraint":
        return Constraint(_Op_code.exists, seq, iter_var, func)

    @staticmethod
    def forall(seq: Union["zython.var_par.types._range",
                          "zython.var_par.types.orig_range",
                          "zython.var_par.array.ArrayMixin",
                          Sequence["zython.var"]],
               iter_var: Optional["zython.var"] = None,
               func: Optional[Union["Constraint", Callable]] = None) -> "Constraint":
        return Constraint(_Op_code.forall, seq, iter_var, func)
