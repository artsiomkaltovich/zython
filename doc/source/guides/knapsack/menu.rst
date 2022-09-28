Menu
====

Here we will try to solve problem described in `xkcd 287 comics <https://xkcd.com/287/>`_.

.. image:: https://imgs.xkcd.com/comics/np_complete.png
  :width: 500
  :alt: General solutions get you 50% tip.

You with friends want to make order in the restaurant and spend exactly $15.05, no more, no less, is it possible?

Naive Model
-----------

.. testcode::

    import zython as zn


    class Model(zn.Model):
        def __init__(self, order_price, menu_price):
            self.menu_price = zn.Array(menu_price)
            self.order = zn.Array(zn.var(zn.range(100)), shape=len(menu_price))
            self.constraints = [
                zn.sum(range(len(menu_price)), lambda i: self.menu_price[i] * self.order[i]) == order_price,
            ]

    def get_receipt(menu_price, order):
        return sum(o * p for o, p in zip(order, menu_price))

    order_price = 1505
    menu_price = [215, 275, 335, 355, 420, 580]
    model = Model(order_price, menu_price)
    result = model.solve_satisfy()
    print(get_receipt(menu_price, result["order"]))

.. testoutput::

    1505

Trying to find better solution
------------------------------

This problem has two possible solutions: ``[7, 0, 0, 0, 0, 0]`` and ``[1, 0, 0, 2, 0, 1]``.
In most cases group of friends will choose the second variant, because they can taste more dishes.
But by default minizinc stops execution if it finds any solution, so you can receive pretty boring
``[7, 0, 0, 0, 0, 0]`` one. You can change it by specifying


::

    model.solve_satisfy(all_solutions=True)


The solver will return every solution for a problem, but such usage can cause some issues:

    #. Finding every solution can be time consuming for some input data
    #. We do learn programming to make machines solve out task completely :)

Another variant is to limit maximum number of portions for every dish:

::

    # maximum 2 portion of any dish are allowed
    self.order = zn.Array(zn.var(zn.range(2)), shape=len(menu_price))

There is also another approach (probably the best one, as it has no hyperparameters):
We can redefine the model to make it choose the most varied order
(order with the biggest number of tasted dishes).

Maximizing Variety
------------------

.. testcode::

    class Model(zn.Model):
        def __init__(self, order_price, menu_price):
            self.menu_price = zn.Array(menu_price)
            self.order = zn.Array(zn.var(zn.range(100)), shape=len(menu_price))
            self.variety = zn.Array(zn.var(zn.range(2)), shape=len(menu_price))
            self.constraints = [
                self.get_order_price() == order_price,
                self.calculate_variety(),
            ]

        def get_order_price(self):
            return zn.sum(zn.range(self.menu_price.size(0)),
                          lambda i: self.menu_price[i] * self.order[i])

        def calculate_variety(self):
            return zn.forall(zn.range(self.menu_price.size(0)),
                             lambda i: (self.order[i] == 0) & (self.variety[i] == 0)
                                        | (self.order[i] > 0) & (self.variety[i] == 1)
                             )


    model = Model(1505, [215, 275, 335, 355, 420, 580])
    result = model.solve_maximize(zn.sum(model.variety))
    print(result["order"])

.. testoutput::

    [1, 0, 0, 2, 0, 1]
