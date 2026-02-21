import zython as zn


def test_2d():
    class MyModel(zn.Model):
        def __init__(self, array):
            self.a = zn.Array(array)
            self.s1 = zn.sum(self.a[0, 1:2])
            self.s2 = zn.sum(self.a[2:, 1:])
            self.s3 = zn.sum(self.a[2:, 2:])

    r = (range(i, i + 3) for i in range(3))
    model = MyModel(((j for j in i) for i in r))
    result = model.solve_satisfy()
    assert result["s1"] == 1
    assert result["s2"] == 7
    assert result["s3"] == 4


def test_3():
    class MyModel(zn.Model):
        def __init__(self, array):
            self.a = zn.Array(array)
            self.s = zn.sum(self.a)
            self.s1 = zn.sum(self.a[:, :, 1:])

    array = [[[1, 2], [3, 4]], [[5, 6], [7, 8]]]
    model = MyModel(array)
    result = model.solve_satisfy()
    assert result["s"] == 36
    assert result["s1"] == 20
