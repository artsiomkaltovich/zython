import pytest

import zython as zn
from zython._compile.zinc.to_str import to_str
from zython.var_par.collections.set import SetPar


class TestCreate:
    def test_int_tuple(self):
        a = zn.Set((1, 2, 3))
        assert isinstance(a, SetPar)
        assert a.value == (1, 2, 3)

    @pytest.mark.parametrize("collection", [zn.range(1, 4), range(1, 4)])
    def test_int_range(self, collection):
        a = zn.Set(collection)
        assert isinstance(a, SetPar)
        assert a.value == collection

    def test_int_generator(self):
        a = zn.Set((a + 1 for a in range(4)))
        assert isinstance(a, SetPar)
        assert a.value == (1, 2, 3, 4)

    @pytest.mark.parametrize("arg", ["aaa", zn.var(float), (a for a in "aaa"), (1.2, 2.5)])
    def test_wrong_type(self, arg):
        with pytest.raises(ValueError, match="Unsupported type for set: <class"):
            zn.Set(arg)


class TestToStr:
    @pytest.mark.parametrize("name, arg", [("a", (1, 2)), ("b", zn.var(range(1, 5)))])
    def test_name(self, name, arg):
        a = zn.Set(arg)
        a._name = name
        assert name == to_str(a)


class TestModel:
    def test(self):
        class Model(zn.Model):
            def __init__(self, ):
                self.a = zn.Set(zn.var(zn.range(5)))
                self.b = zn.Set(zn.range(10))

        m = Model()
        s = m.compile("satisfy").split(";")
        src = [line.strip() for line in s]
        assert "set of  0..9: b" == src[0]
        assert "var set of  0..4: a" == src[1]
