CryptArithmetic Problem
=======================

In such kind of problem all letters should be replaced with digits with two
main restriction:

- equation should be hold
- the same digit can't be assign to different letters and vise versa.

The very common example of such problem is the following:

::

        S E N D
    +   M O R E
    = M O N E Y

Let's express it with zython.

Python Model
------------

.. testcode::

    import zython as zn


    class MoneyModel(zn.Model):
        def __init__(self):
            self.S = zn.var(range(1, 10))
            self.E = zn.var(range(0, 10))
            self.N = zn.var(range(0, 10))
            self.D = zn.var(range(0, 10))
            self.M = zn.var(range(1, 10))
            self.O = zn.var(range(0, 10))
            self.R = zn.var(range(0, 10))
            self.Y = zn.var(range(0, 10))

            self.constraints = [(self.S * 1000 + self.E * 100 + self.N * 10 + self.D +
                                 self.M * 1000 + self.O * 100 + self.R * 10 + self.E ==
                                 self.M * 10000 + self.O * 1000 + self.N * 100 + self.E * 10 + self.Y),
                                 zn.alldifferent((self.S, self.E, self.N, self.D, self.M, self.O, self.R, self.Y))]

    model = MoneyModel()
    result = model.solve_satisfy()
    print(" ", result["S"], result["E"], result["N"], result["D"])
    print(" ", result["M"], result["O"], result["R"], result["E"])
    print(result["M"], result["O"], result["N"], result["E"], result["Y"])

.. testoutput::

      9 5 6 7
      1 0 8 5
    1 0 6 5 2
