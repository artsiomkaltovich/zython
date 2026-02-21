Fibonacci number
================

Common exercise for learning new programming language is calculation of
`Fibonacci numbers <https://en.wikipedia.org/wiki/Fibonacci_number>`_, let look how we can express
model for such calculation in zython.

Python Model
------------

.. testcode::

    import zython as zn


    class MyModel(zn.Model):
        def __init__(self, n):
            if n < 1:
                raise ValueError("N should be positive integer")
            elif n == 1:
                self.a = zn.Array([1])
            elif n == 2:
                self.a = zn.Array([1, 1])
            else:
                self.a = zn.Array(zn.var(int), shape=n)

            self.constraints = [self.a[0] == 1, self.a[1] == 1,
                                zn.forall(range(2, n), lambda i: self.a[i] == self.a[i - 1] + self.a[i - 2])]

    model = MyModel(10)
    result = model.solve_satisfy()
    print(result["a"])

.. testoutput::

    [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
