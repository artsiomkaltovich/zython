from zython.operations import _iternal
from zython.operations._op_codes import _Op_code
from zython.operations._constraint import _Constraint
from zython.operations._operation import _Operation
from zython.var_par.array import ArrayMixin


class alldifferent(_Constraint):
    # TODO: array support?
    def __init__(self, *params):
        super().__init__(_Op_code.alldifferent, params)


class circuit(_Constraint):
    def __init__(self, array):
        super().__init__(_Op_code.circuit, array)


def exists(seq, func=None):
    iter_var, operation = _iternal.get_iter_var_and_op(seq, func)
    return _Operation(_Op_code.exists, seq, iter_var, operation)


def forall(seq, func=None):
    iter_var, operation = _iternal.get_iter_var_and_op(seq, func)
    return _Operation(_Op_code.forall, seq, iter_var, operation)


def sum(seq, func=None):
    iter_var, operation = _iternal.get_iter_var_and_op(seq, func)
    if isinstance(seq, ArrayMixin) and operation is None:
        type_ = seq.type
    else:
        type_ = operation.type
    if type_ is None:
        raise ValueError("Can't derive the type of {} expression".format(func))
    return _Operation(_Op_code.sum_, seq, iter_var, operation, type_=type_)
