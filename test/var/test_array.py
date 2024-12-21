import re

import pytest

import zython as zn
from zython.operations._op_codes import _Op_code


@pytest.mark.parametrize(
    "array",
    [[1, 2, 3, 4], (1, 2, 3, 4), (i + 1 for i in range(4))],
    ids=["list", "tuple", "genexpr"],
)
def test_creating(array):
    class MyModel(zn.Model):
        def __init__(self, array):
            self.a = zn.Array(array)

    model = MyModel(array)
    assert model.a._shape == (4,)


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
            self.s1 = zn.sum(self.a[0, 1:2, :])
            self.s2 = zn.sum(self.a[2:, 1:, :])
            self.s3 = zn.sum(self.a[2:, 2:, :])

    r = ((range(i, i + 3) for i in range(2)) for _ in range(4))
    model = MyModel(((j for j in i) for i in r))
    assert model.a._shape == (4, 2, 3)
    assert model.a.value == [
        [[0, 1, 2], [1, 2, 3]],
        [[0, 1, 2], [1, 2, 3]],
        [[0, 1, 2], [1, 2, 3]],
        [[0, 1, 2], [1, 2, 3]],
    ]


@pytest.mark.parametrize(
    "array", ([1, 0.0], ((1, 0.0), (1, 3)), [[1, 3], [1, "a"]], (((1, "a"),),))
)
def test_different_types(array):
    class MyModel(zn.Model):
        def __init__(self, array):
            self.a = zn.Array(array)

    with pytest.raises(
        ValueError, match="All elements of the array should be the same type"
    ):
        MyModel(array)


def test_var_array_without_shape():
    with pytest.raises(ValueError, match="shape wasn't specified"):
        zn.Array(zn.var(int))


@pytest.mark.parametrize(
    "array", (zn.Array([[1], [2]]), zn.Array(zn.var(int), shape=(1, 2)))
)
@pytest.mark.parametrize("indexes", ((2, 0), (0, 2)))
def test_array_index_error(array, indexes):
    with pytest.raises(IndexError):
        array[indexes]


@pytest.mark.parametrize(
    "array", (((1, 0, 1), (1, 3)), [[1, 3], [1, 1, 0]], (((1, 1), 1),))
)
def test_different_length(array):
    class MyModel(zn.Model):
        def __init__(self, array):
            self.a = zn.Array(array)

    with pytest.raises(
        ValueError, match="Subarrays of different length are not supported"
    ):
        MyModel(array)


class TestPos:
    def test_int_1d(self):
        a = zn.Array([1, 2, 3])
        a = a[1]
        assert a.pos == (1,)

    def test_2d_index_on_1d_array(self):
        a = zn.Array([1, 2, 3])
        with pytest.raises(
            ValueError, match="The array has 1 dimensions, but 2 indexes were specified"
        ):
            _ = a[1, 0]

    @pytest.mark.parametrize(
        "array, pos, error",
        [
            (
                zn.Array([[1, 2]]),
                4,
                "The array has 2 dimensions, but 1 indexes were specified",
            ),
            (
                zn.Array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]]),
                (slice(1, 2), slice(2, 4)),
                "The array has 3 dimensions, but 2 indexes were specified",
            ),
        ],
    )
    def test_not_every_index(self, array, pos, error):
        with pytest.raises(ValueError, match=error):
            array[pos]

    def test_neg_int(self):
        a = zn.Array([1, 2, 3])
        with pytest.raises(
            ValueError, match="Negative indexes are not supported for now"
        ):
            _ = a[-1]

    def test_step(self):
        a = zn.Array([1, 2, 3])
        with pytest.raises(
            ValueError, match="step other then 1 isn't supported, but it is 2"
        ):
            _ = a[1:3:2]

    @pytest.mark.parametrize("pos", [slice(-1, 2), slice(1, -2), slice(-1, -2)])
    @pytest.mark.parametrize("before", (True, False))
    def test_neg_slice_2d(self, pos, before):
        a = zn.Array([[1], [2], [3]])
        with pytest.raises(
            ValueError, match="Negative indexes are not supported for now"
        ):
            _ = a[:, pos] if before else a[pos, :]

    @pytest.mark.parametrize("start", (10, 15))
    def test_slice_wrong_start(self, start):
        array = zn.Array(zn.var(int), shape=(3, 2, 4))
        with pytest.raises(
            ValueError,
            match=re.escape(f"start({start}) should be smaller then stop(10)"),
        ):
            _ = array[1, start:10, :]

    @pytest.mark.parametrize(
        "pos, expected", [((0, 1), (0, 1)), ((0, slice(1, 3)), (0, slice(1, 3, 1)))]
    )
    def test_2d(self, pos, expected):
        a = zn.Array([[1, 2], [2, 3], [3, 4]])
        a = a[pos]
        assert a.pos == expected


class TestSize:
    @pytest.mark.parametrize("dim", (-1, 3))
    def test_wrong_dim(self, dim):
        a = zn.Array([[1, 2], [2, 3], [3, 4]])
        with pytest.raises(
            ValueError,
            match=f"The array has 0\\.\\.2 dimensions, but {dim} were specified",
        ):
            a.size(dim)

    @pytest.mark.parametrize(
        "array",
        [zn.Array([[1, 2], [2, 3], [3, 4]]), zn.Array(zn.var(int), shape=(3, 2))],
    )
    @pytest.mark.parametrize("dim, expected", ((0, 3), (1, 2)))
    def test_dim(self, array, dim, expected):
        class MyModel(zn.Model):
            def __init__(self, array):
                self.a = array
                self.s = self.a.size(dim)
                self.s2 = self.a.size(dim) * 2  # test arithmetic operations
                self.s_bigger_2 = self.a.size(dim) > 2  # test compare operations
                assert self.s.type is int
                assert self.s2.type is int
                assert self.s_bigger_2.type is int

        result = MyModel(array).solve_satisfy()
        assert result["s"] == expected
        assert result["s_bigger_2"] == (expected > 2)
        assert result["s2"] == (expected * 2)
