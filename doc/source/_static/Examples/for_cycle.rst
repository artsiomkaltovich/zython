Collection Iteration (For Cycle)
================================

Arrays are collections of variables or parameters of the same type. Length of the array can't be changed during
model solving.

Different Neighbour
-------------------

Let create a basic model as an example of array usage. The model will create an array and fill it with integer values
with two constraints:

- All values should be positive
- The value of item shouldn't be the same as the value of the previous and the next item.

.. testcode::

    import zython as zn

    class DifferentNeighbour(zn.Model):
        def __init__(self, length):
            self.a = zn.Array(zn.var(int), length)

            self.constraints = [all(i > 0 for i in self.a)]

    model = DifferentNeighbour(10)
    result = model.solve_satisfy()
    print(result["a"])

.. testoutput::

    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
