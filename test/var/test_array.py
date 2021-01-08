import pytest

import zython as zn


@pytest.mark.parametrize("array", [[1, 2, 3, 4], (1, 2, 3, 4), (i + 1 for i in range(4))],
                         ids=["list", "tuple", "genexpr"])
def test_creating(array):
    class MyModel(zn.Model):
        def __init__(self, array):
            self.a = zn.Array(array)

    model = MyModel(array)
    assert model.a._shape == (4, )


def test_2d_correct():
    class MyModel(zn.Model):
        def __init__(self, array):
            self.a = zn.Array(array)

    array = [[1, 2, 3], [1, 3, 5]]
    model = MyModel(array)
    assert model.a._shape == (2, 3)
    assert model.a.value == array


def test_2d_gen():
    class MyModel(zn.Model):
        def __init__(self, array):
            self.a = zn.Array(array)
            self.s1 = zn.sum(self.a[0, 1:2])
            self.s2 = zn.sum(self.a[2:, 1:])
            self.s3 = zn.sum(self.a[2:, 2:])

    r = (range(i, i + 3) for i in range(2))
    model = MyModel(((j for j in i) for i in r))
    assert model.a._shape == (2, 3)
    assert model.a.value == [[0, 1, 2], [1, 2, 3]]


def test_3d_gen():
    class MyModel(zn.Model):
        def __init__(self, array):
            self.a = zn.Array(array)
            self.s1 = zn.sum(self.a[0, 1:2])
            self.s2 = zn.sum(self.a[2:, 1:])
            self.s3 = zn.sum(self.a[2:, 2:])

    r = ((range(i, i + 3) for i in range(2)) for _ in range(4))
    model = MyModel(((j for j in i) for i in r))
    assert model.a._shape == (4, 2, 3)
    assert model.a.value == [[[0, 1, 2], [1, 2, 3]], [[0, 1, 2], [1, 2, 3]], [[0, 1, 2], [1, 2, 3]], [[0, 1, 2], [1, 2, 3]]]


@pytest.mark.parametrize("array", ([1, 0.0], ((1, 0.0), (1, 3)), [[1, 3], [1, "a"]], (((1, "a"), ), )))
def test_different_types(array):
    class MyModel(zn.Model):
        def __init__(self, array):
            self.a = zn.Array(array)

    with pytest.raises(ValueError, match="All elements of the array should be the same type"):
        MyModel(array)


def test_var_array_without_shape():
    with pytest.raises(ValueError, match="shape wasn't specified"):
        zn.Array(zn.var(int))


@pytest.mark.parametrize("array", (zn.Array([[1], [2]]), zn.Array(zn.var(int), shape=(1, 2))))
@pytest.mark.parametrize("indexes", ((2, 0), (0, 2)))
def test_array_index_error(array, indexes):
    with pytest.raises(IndexError):
        array[indexes]


@pytest.mark.parametrize("array", (((1, 0, 1), (1, 3)), [[1, 3], [1, 1, 0]], (((1, 1), 1), )))
def test_different_length(array):
    class MyModel(zn.Model):
        def __init__(self, array):
            self.a = zn.Array(array)

    with pytest.raises(ValueError, match="Subarrays of different length are not supported"):
        MyModel(array)


class TestPos:
    def test_int_1d(self):
        a = zn.Array([1, 2, 3])
        a = a[1]
        assert a.pos == (1,)

    def test_tuple_1d(self):
        a = zn.Array([1, 2, 3])
        with pytest.raises(ValueError, match="Array has 1 dimensions but 2 were specified"):
            _ = a[1, 0]

    def test_neg_int(self):
        a = zn.Array([1, 2, 3])
        with pytest.raises(ValueError, match="Negative indexes are not supported for now"):
            _ = a[-1]

    def test_step(self):
        a = zn.Array([1, 2, 3])
        with pytest.raises(AssertionError, match="Step other then 1 isn't supported for now"):
            _ = a[1:3:2]

    @pytest.mark.parametrize("pos", [slice(-1, 2), slice(1, -2), slice(-1, -2)])
    def test_neg_slice_2d(self, pos):
        a = zn.Array([[1], [2], [3]])
        with pytest.raises(ValueError, match="Negative indexes are not supported for now"):
            _ = a[pos]

    @pytest.mark.parametrize("pos, expected", [((0, 1), (0, 1)),
                                               ((0, slice(1, 3)), (0, slice(1, 3, 1)))])
    def test_2d(self, pos, expected):
        a = zn.Array([[1, 2], [2, 3], [3, 4]])
        a = a[pos]
        assert a.pos == expected

    @pytest.mark.parametrize("pos, expected", [(1, (1, slice(None, None, 1))),
                                               (slice(None, 2), (slice(None, 2, 1), slice(None, None, 1))),
                                               (slice(1, None), (slice(1, None, 1), slice(None, None, 1)))])
    def test_2d_added_last_dim(self, pos, expected):
        a = zn.Array([[1, 2], [2, 3], [3, 4]])
        a = a[pos]
        assert a.pos == expected


class TestSize:
    @pytest.mark.parametrize("dim", (-1, 3))
    def test_wrong_dim(self, dim):
        a = zn.Array([[1, 2], [2, 3], [3, 4]])
        with pytest.raises(ValueError, match=f"Array has 0\\.\\.2 dimensions, but {dim} were specified"):
            a.size(dim)
