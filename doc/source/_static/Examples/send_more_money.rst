CryptArithmetic Problem
=======================

In such kind of problem all letters should be replaced with digits with two
main restriction:

- equation will be true
- the same digit can't be assign to different letters and vise versa.

The very common example of such problem is the following:

::

    S E N D
+   M O R E
= M O N E Y

Let's express it with zython.

Python Model
============

.. testcode::

    import zython as zn

    class MoneyModel(zn.Model):
        def __init__(self):
            self.S = zn.var(int)
            self.E = zn.var(int)
            self.N = zn.var(int)
            self.D = zn.var(int)
            self.M = zn.var(int)
            self.O = zn.var(int)
            self.R = zn.var(int)
            self.Y = zn.var(int)

The result is:

.. testoutput::

                     Time  PRICE   AVERAGE   STDDEV  LOWER_BAND  UPPER_BAND
    0 2003-12-01 00:00:00  1.45   1.450000  0.00000  1.450000    1.450000
    1 2003-12-01 00:00:01  1.55   1.500000  0.05000  1.450000    1.550000
    2 2003-12-01 00:00:02  1.45   1.483333  0.04714  1.436193    1.530474
    3 2003-12-01 00:00:04  1.30   1.375000  0.07500  1.300000    1.450000
    4 2003-12-01 00:00:10  1.40   1.400000  0.00000  1.400000    1.400000

