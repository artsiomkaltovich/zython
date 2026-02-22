``Array.ndims`` and ``Array.size`` Methods
==========================================

`Zython` provides the way of customization and retrospection of the array in the model in order to get its number of
dimension and number of items in every dimensions.

``Array.ndims()`` will return number of dimensions is the array, this function is totally evaluated by python code,
because `Zython` doesn't support model with variable number of dimension of any array. While ``Array.size(dim)``
returns operation which later will be evaluated by the solver, so you can parametrize your model with the arrays of
different size, but not number of dimensions.

Python Model
------------

.. testcode::

    import zython as zn


    class MyModel(zn.Model):
        def __init__(self, arr):
            self.a = zn.Array(arr)
            print(self.a.ndims())
            self.size0 = self.a.size(0)
            self.size1 = self.a.size(1)

    model = MyModel([[1, 2], [3, 4]])
    result = model.solve_satisfy()
    print(result)
    model = MyModel([[1], [2], [3]])
    result = model.solve_satisfy()
    print(result)

.. testoutput::

    2
    Solution(size0=2, size1=2)
    2
    Solution(size0=3, size1=1)
