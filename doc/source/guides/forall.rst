``zn.forall`` Constraint
========================

``zn.forall`` constraint is used for defining constraint which should be satisfied for all specified elements of the
array.

Let's define model which will find array of the length n, all elements of which are positive and no the same element are
placed on the two adjacent positions.

Python Model
------------

.. testcode::

    import zython as zn


    class MyModel(zn.Model):
        def __init__(self, n):
            self.a = zn.Array(zn.var(int), shape=n)

            self.constraints = [zn.forall(range(n - 1), lambda i: self.a[i] != self.a[i + 1]),
                                zn.forall(self.a, lambda elem: elem > 0)]

    model = MyModel(5)
    result = model.solve_satisfy()
    print(result["a"])

.. testoutput::

    [2, 1, 2, 1, 2]
