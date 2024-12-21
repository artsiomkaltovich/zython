import re

import pytest

import zython as zn
from zython.operations._iternal import get_iter_var_and_op
from zython.operations._op_codes import _Op_code


def test_range_and_lambda():
    iter_var, op = get_iter_var_and_op(range(5), lambda i: i > 1)
    assert iter_var.name == "i"
    assert iter_var.type is int
    assert op.op == _Op_code.gt
    assert op.params[0].name == "i"
    assert isinstance(op.params[1], int) and op.params[1] == 1


def test_slice_and_func():
    def fn(par):
        return 2 - par

    array = zn.Array(zn.var(int), shape=(3, 4))
    iter_var, op = get_iter_var_and_op(array[2:, :], fn)
    assert iter_var.name == "par"
    assert iter_var.type is int
    assert op.op == _Op_code.sub
    assert isinstance(op.params[0], int) and op.params[0] == 2
    assert op.params[1].name == "par"


def test_array_and_op():
    array = zn.Array(zn.var(int), shape=(3, 4))
    v = zn.var(int)
    iter_var, op = get_iter_var_and_op(array, v + 1)
    assert op.op == _Op_code.add
    assert isinstance(op.params[1], int) and op.params[1] == 1
    assert isinstance(op.params[0], zn.var) and op.params[0] is v


def test_no_arg_func():
    def fn():
        return -1
    iter_var, op = get_iter_var_and_op([1, 2, 3], fn)
    assert isinstance(op, int) and op == -1


def test_too_many_params():
    with pytest.raises(ValueError, match="only functions and lambdas with one arguments are supported"):
        get_iter_var_and_op(range(5), lambda i, y: 1)


def test_wrong_seq():
    with pytest.raises(Exception, match=re.escape("<class 'str'> isn't supported, please use Sequence or Array here")):
        get_iter_var_and_op("abc", lambda i: 1)


def test_empty_seq():
    with pytest.raises(ValueError, match="empty sequences are not supported as constraint parameter"):
        get_iter_var_and_op(tuple(), lambda i: 1)
