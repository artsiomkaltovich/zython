Supported Types of Variables
============================

Latest version of zython supports variables and parameters of
integer and float types, and ranges from them.

The example with integer fields is specified in
:ref:`the previous file <model-structure>`. In this tutorial we
will see examples of creating models with fields of other fields.

Float Fields
------------

Float fields can be created as integer fields
with the same syntax: just return input parameter increased by 1.0.

::

    self.a = zn.par(3.14)
    self.b = zn.var(float)

Lets create a model, which use float fields, it will be pretty
stupid: just find

.. testcode::

    import zython as zn

    class Model(zn.Model):
        def __init__(self, a):
            self.a = zn.par(a)
            self.x = zn.var(float)
            self.constraints = [self.x == self.a + 1]

    m = Model(2.4)
    result = m.solve_satisfy(solver="cbc")
    print(result["x"])

.. testoutput::

    3.4

.. warning::

    Not every solver fully supports float variables,
    to learn more about solvers, please see
    :ref:`documentation <solvers>` for them.

Ranges
------

Zython specifies ``zn.range`` type, which can be initialized
by both int and float variables, as well as zython expressions.

.. warning::

    ``zn.range`` doesn't support step argument for now.

.. deprecated:: 0.2

    ``zython`` doesn't redefine builtin range function,
    so to create ranges with float or zython's par/var
    types, use ``zn.range`` function.

Lets look at the example of simple model, which calculates
the center between two number.

.. testcode::

    class Model(zn.Model):
        def __init__(self, left, right):
            self.center = zn.var(zn.range(left, right))
            self.constraints = [self.center == (left + right) / 2]

    m = Model(1.3, 5.7)
    result = m.solve_satisfy()
    print(result["center"])

.. testoutput::

    3.5
