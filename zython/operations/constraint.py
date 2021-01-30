from typing import Union, Optional, Callable

import zython
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


def _exists(seq: "zython.var_par.types.ZnSequence",
            iter_var: Optional["zython.var"] = None,
            func: Optional[Union["Constraint", Callable]] = None) -> "Constraint":
    return Constraint(_Op_code.exists, seq, iter_var, func)


def _forall(seq: "zython.var_par.types.ZnSequence",
            iter_var: Optional["zython.var"] = None,
            func: Optional[Union["Constraint", Callable]] = None) -> "Constraint":
    return Constraint(_Op_code.forall, seq, iter_var, func)
