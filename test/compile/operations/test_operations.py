import operator
from typing import Callable

import pytest
import zython as zn
from zython._compile.zinc.to_str import to_str


class TestBinary:
    v = zn.var(int)
    v._name = "i"
    p = zn.par(2)
    p._name = "a"
    variables = v, p

    @pytest.mark.parametrize("v", variables)
    @pytest.mark.parametrize("op, sign", ([operator.add, "+"], [operator.sub, "-"],
                                          [operator.floordiv, "div"], [operator.mul, "*"], [operator.mod, "mod"],
                                          [operator.eq, "=="], [operator.ne, "!="],
                                          [operator.gt, ">"], [operator.lt, "<"],
                                          [operator.ge, ">="], [operator.le, "<="]))
    def test_simple_ariph_binary_op(self, v, op: Callable, sign: str):
        result = op(v, 1)
        assert to_str(result) == f"({v.name} {sign} 1)"
        assert result.type is int

    def test_complex_binary_op(self):
        result = (1 - self.v) * (2 // self.p) >= 4
        assert to_str(result) == f"(((1 - {self.v.name}) * (2 div {self.p.name})) >= 4)"
        assert result.type is int

    def test_long_binary_op(self):
        result = 1 + self.v * 2 - self.p + self.v ** self.p
        assert to_str(result) == f"(((1 + ({self.v.name} * 2)) - {self.p.name}) + pow({self.v.name}, {self.p.name}))"
        assert result.type is int

    def test_pow_bracket(self):
        result = -3 * self.v ** (2 % self.p)
        assert to_str(result) == f"(-3 * pow({self.v.name}, (2 mod {self.p.name})))"
        assert result.type is int

    def test_wrong_pow(self):
        with pytest.raises(ValueError, match="modulo is not supported"):
            pow(self.p, 2, 10)

    def test_wrong_div(self):
        with pytest.raises(ValueError, match="right part of expression can't be 0"):
            self.v // 0

    def test_wrong_mod(self):
        with pytest.raises(ValueError, match="right part of expression can't be 0"):
            self.v % 0

    @pytest.mark.parametrize("op, sign", ((operator.and_, "/\\"), (operator.or_, "\\/"), (operator.xor, "xor")))
    def test_binary_logical(self, op, sign):
        result = op(self.p > self.v, 2 > self.v)
        assert to_str(result) == f"(({self.p.name} > {self.v.name}) {sign} ({self.v.name} < 2))"

    def test_invert(self):
        result = ~(self.p < self.v)
        assert to_str(result) == f"(not ({self.p.name} < {self.v.name}))"
