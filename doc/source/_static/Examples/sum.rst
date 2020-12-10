Initialization of Variables with Array and Sum
==============================================

Python Model
------------

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
