Model Structure
===============

In minizinc every model is a collection of variables,
parameters and constraints.

Parameters and Variables
------------------------

Variables are unknown values which should be found by solver,
parameters are some constants which are known during model evaluation,
you can change parameters from run to run, and this will, obviously,
affect result. E.g. number of cities and distances between them
are parameters for traveling salesman problem,
the path will depends on them, but the programmer can create one model
for the problem and then just execute it for different parameters
without model source code changes.

We will start with a simple (or even stupid) model:

- declare parameter `n` - `natural number <https://en.wikipedia.org/wiki/Natural_number>`_.
- find variable `v` which is the next natural number.

Parameters and Variables Definition
:::::::::::::::::::::::::::::::::::

Parameters and variables are defined by ``zn.par`` and ``zn.var`` functions.

In the models, described above, the definition will be the following:

::

    class Model(zn.Model):
        def __init__(self, n):
            self.n = zn.par(n)
            self.v = zn.var(int)

Constraints
-----------
Constraints are constraints :) which should be satisfied by
variables values.

Constraints Definition
::::::::::::::::::::::

Constraints are defined as a collection of expression of model
arguments in ``self.constraints`` field.

In our test model you should add the following line in init,
which says, `v` should be the next number after `n`.

::

    self.constraints = [self.v == self.n + 1]

All in One Model
----------------

So all in one example of the model, that is looking for
the next natural number is:

.. testcode::

    import zython as zn

    class Model(zn.Model):
        def __init__(self, n):
            self.n = zn.par(n)
            self.v = zn.var(int)
            self.constraints = [self.v == self.n + 1]

    # and here is usage of the model
    model = Model(2)
    result = model.solve_satisfy()
    print(result["v"])
    model = Model(4)
    result = model.solve_satisfy()
    print(result["v"])

.. testoutput::

    3
    5
