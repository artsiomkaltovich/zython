import pytest
import zython as zn


@pytest.mark.parametrize("array", [[1, 2, 3, 4], (1, 2, 3, 4), (i + 1 for i in range(4))],
                         ids=["list", "tuple", "genexpr"])
def test_creating(array):
    class MyModel(zn.Model):
        def __init__(self, array):
            self.a = zn.Array(array)

    model = MyModel(array)
    assert model.a.value == (1, 2, 3, 4)
    assert model.a.shape == (4, )
    assert len(model.a) == 4
