import zython as zn


def test_2d():
    class MyModel(zn.Model):
        def __init__(self, array):
            self.a = zn.Array(array)
            self.p1 = zn.product(self.a[0, 1:2])
            self.p2 = zn.product(self.a[2:, 1:])
            self.p3 = zn.product(self.a[2:, 2:])

    model = MyModel([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    result = model.solve_satisfy()
    assert result["p1"] == 2
    assert result["p2"] == 72
    assert result["p3"] == 9


def test_3():
    class MyModel(zn.Model):
        def __init__(self, array):
            self.a = zn.Array(array)
            self.p = zn.product(self.a)
            self.p1 = zn.product(self.a[:, 1:, :])

    array = [[[1, 2], [3, 4]], [[5, 6], [7, 8]]]
    model = MyModel(array)
    result = model.solve_satisfy()
    assert result["p"] == 40320
    assert result["p1"] == 672


def test_1():
    class MyModel(zn.Model):
        def __init__(self, array):
            self.a = zn.Array(array)
            self.p = zn.product(self.a)

    array = [1, 2, 3, 4, 5, 6, 7, 8]
    model = MyModel(array)
    result = model.solve_satisfy()
    assert result["p"] == 40320


def test_empty():
    class MyModel(zn.Model):
        def __init__(self):
            self.a = zn.Array([1, 2])
            self.p = zn.product(self.a[3:])

    model = MyModel()
    result = model.solve_satisfy()
    assert result["p"] == 1
