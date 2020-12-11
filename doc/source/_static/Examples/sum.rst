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
