import pytest
import zython as zn


@pytest.mark.parametrize("array", [[1, 2, 3, 4], (1, 2, 3, 4), (i + 1 for i in range(4))],
                         ids=["list", "tuple", "genexpr"])
def test_creating(array):
    class MyModel(zn.Model):
        def __init__(self, array):
            self.a = zn.Array(array)

    model = MyModel(array)
    assert model.a.shape == (4, )
    assert len(model.a) == 4


def test_2d_correct():
    class MyModel(zn.Model):
        def __init__(self, array):
            self.a = zn.Array(array)

    model = MyModel([[1, 2], [1, 3]])
    assert model.a.shape == (2, 2)
    assert len(model.a) == 2


@pytest.mark.parametrize("array", ([1, 0.0], ((1, 0.0), (1, 3)), [[1, 3], [1, "a"]], (((1, "a"), ), )))
def test_different_types(array):
    class MyModel(zn.Model):
        def __init__(self, array):
            self.a = zn.Array(array)

    with pytest.raises(ValueError, match="All elements of the array should be the same type"):
        MyModel(array)


@pytest.mark.parametrize("array", (((1, 0, 1), (1, 3)), [[1, 3], [1, 1, 0]], (((1, 1), 1), )))
def test_different_length(array):
    class MyModel(zn.Model):
        def __init__(self, array):
            self.a = zn.Array(array)

    with pytest.raises(ValueError, match="Subarrays of different length are not supported"):
        MyModel(array)
