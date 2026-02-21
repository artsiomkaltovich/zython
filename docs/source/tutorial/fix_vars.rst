Assigning Values to Variables
=============================

In minizinc models you can specify some variable and later
assign values to them and calculates values of others variables
(unassigned ones).
This helps reuse models: one model can be used for several calculation.

Lets rewrite
`the bank loan sample <https://www.minizinc.org/doc-2.6.4/en/modelling.html#real-number-solving>`_
from the official minizinc documentation to a zython model.

The example describes problem of taking out a short loan for one year
to be repaid in 4 quarterly instalments.

Zython Model
------------

In the following model:

- ``i`` is an interest
- ``p`` is a loan amount
- ``r`` is an instalments (amount the customer pays every quarter)
- ``b`` is an array with the payer's debt after every instalment
- ``last_b`` is the payer debt after all instalments

.. testcode::

    from typing import Optional

    import zython as zn


    class MyModel(zn.Model):
        def __init__(
                self,
                i: float,
                p: Optional[float] = None,
                r: Optional[float] = None,
                last_b: Optional[float] = None,
        ):
            super().__init__()
            self.p = zn.var(float, p)
            self.r = zn.var(float, r)
            self.i = zn.var(zn.range(0.0, 10.0), i)
            self.b = zn.Array(zn.var(float), shape=(4,))
            self.constraints = [
                self.b[0] == self.p * (1.0 + self.i) - self.r,
                zn.forall(range(1, 4), lambda j: self.b[j] == self.b[j - 1] * (1.0 + self.i) - self.r),
            ]
            if last_b is not None:
                self.constraints += [self.b[3] == last_b]

Usage
-----

If you run the model as is it will fail, because too high level
of uncertainty. But you can fix some variables by assigning values
to them.

What will be your debt if you take 1000 with 4% interest and 4 instalments
and will pay 260 as every instalment?

.. testcode::

    model = MyModel(0.04, p=1000.0, r=260.0)
    result = model.solve_satisfy(solver="cbc")
    print(f"{result['b'][-1]:.2f}")


.. testoutput::

    65.78

How big should be the instalment
if you take 1000 with 4% interest and 4 instalments
so after last instalment the debt will be zero.

.. testcode::

    model = MyModel(0.04, p=1000.0, last_b=0.0)
    result = model.solve_satisfy(solver="cbc")
    print(f"{result['r']:.2f}")


.. testoutput::

    275.49

How much you can take as a loan with 4% interest and 4 instalments
if you pay 250 as every instalment.

.. testcode::

    model = MyModel(0.04, r=250.0, last_b=0.0)
    result = model.solve_satisfy(solver="cbc")
    print(f"{result['p']:.2f}")


.. testoutput::

    907.47
