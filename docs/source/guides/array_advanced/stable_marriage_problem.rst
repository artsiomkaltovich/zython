Stable Marriage Problem
=======================

This guide demonstrates how to model the classic Stable Marriage Problem using zython arrays and advanced constraints.

Problem Description
-------------------
Given *n* men and *n* women, each with their own preference rankings for the opposite group, the goal is to find a stable matching such that no man and woman would both prefer each other over their assigned partners.

The model is based on the example from the `MiniZinc documentation <https://docs.minizinc.dev/en/2.9.0/modelling2.html#array-access-constraints>`_.


Python Model
------------

.. testcode::

    import zython as zn
    from itertools import product

    n = 5
    rank_women = [
        [1, 2, 4, 3, 5],
        [3, 5, 1, 2, 4],
        [5, 4, 2, 1, 3],
        [1, 3, 5, 4, 2],
        [4, 2, 3, 5, 1],
    ]
    rank_men = [
        [5, 1, 2, 4, 3],
        [4, 1, 3, 2, 5],
        [5, 3, 2, 4, 1],
        [1, 5, 4, 3, 2],
        [4, 3, 2, 1, 5],
    ]

    class MyModel(zn.Model):
        def __init__(self, rank_women, rank_men):
            n = len(rank_women)
            self.rank_women = zn.Array(rank_women)
            self.rank_men = zn.Array(rank_men)
            self.husband = zn.Array(zn.var(range(n)), shape=(n,))
            self.wife = zn.Array(zn.var(range(n)), shape=(n,))
            self.constraints = [
                zn.forall(range(n), lambda m: self.husband[self.wife[m]] == m),
                zn.forall(range(n), lambda w: self.wife[self.husband[w]] == w),
                zn.forall(
                    range(n),
                    range(n),
                    lambda m, o: zn.implication(
                        self.rank_men[m, o] < self.rank_men[m, self.wife[m]],
                        self.rank_women[o, self.husband[o]] < self.rank_women[o, m],
                    ),
                ),
                zn.forall(
                    range(n),
                    range(n),
                    lambda w, o: zn.implication(
                        self.rank_women[w, o] < self.rank_women[w, self.husband[w]],
                        self.rank_men[o, self.wife[o]] < self.rank_men[o, w],
                    ),
                ),
            ]

    model = MyModel(rank_women, rank_men)
    result = model.solve_satisfy()
    print(result)
    assert str(result) == "Solution(husband=[3, 0, 1, 4, 2], wife=[1, 2, 4, 0, 3])"

Explanation
-----------
- Each man and woman is assigned a partner (wife/husband) as a variable.
- The first two constraints ensure the assignments are consistent (inverses).
- The last two constraints enforce stability: no pair prefers each other over their assigned partners.

Output
------

.. testoutput::

    Solution(husband=[3, 0, 1, 4, 2], wife=[1, 2, 4, 0, 3])
