Initialization of Variables with Array and Sum
==============================================

Model's variables and parameters can be initialized as array or expression. The following example shows this concept.
It is the toy example, it is better to solve such models with python, because there are no solution, just calculations,
but it shows the usage of array and array functions.

Sum of 1d Array
---------------

.. testcode::

    import zython as zn

    class MyModel(zn.Model):
        def __init__(self, array):
            self.a = zn.Array(array)
            self.s = zn.sum(self.a)

    model = MyModel([1, 2, 3, 4])
    result = model.solve_satisfy()
    print(result["s"])

.. testoutput::

    10

Partial Sum of 2d Array
-----------------------

.. testcode::

    import zython as zn

    class MyModel(zn.Model):
        def __init__(self, array):
            self.a = zn.Array(array)
            self.s = zn.sum(self.a[:, 1:2])

    model = MyModel([[1, 2, 3], [4, 5, 6]])
    result = model.solve_satisfy()
    print(result["s"])

.. testoutput::

    7

2D Array, Where Every Element is The Sum of The Previous Elements in The Row and The Column
-------------------------------------------------------------------------------------------

.. testcode::

    from pprint import pprint

    import zython as zn


    class MyModel(zn.Model):
        def __init__(self, n):
            self.a = zn.Array(zn.var(int), (n, n))

            self.constraints = [
                # init first values, so model wan't stuck at all zeroes
                self.a[0, 0] == 0, self.a[0, 1] == 1, self.a[1, 0] == 1,
                # init first row and column
                zn.forall(range(2, n), lambda i: (self.a[0, i] == zn.sum(self.a[0, 0:i]))
                                                 & (self.a[i, 0] == zn.sum(self.a[0:i, 0]))),
                # init other items
                zn.forall(range(1, n),
                          lambda i: zn.forall(range(1, n),
                                              lambda j: self.a[i, j]
                                                        == zn.sum(self.a[i, 0:j]) + zn.sum(self.a[0:i, j])))
            ]


    model = MyModel(5)
    result = model.solve_satisfy()
    pprint(result["a"])


.. testoutput::

    [[0, 1, 1, 2, 4], [1, 2, 4, 9, 20], [1, 4, 10, 26, 65], [2, 9, 26, 74, 200], [4, 20, 65, 200, 578]]
