Bakery Profit Maximization
==========================

Let's imagine you've decided host charity event and you will sold cakes to raise some money. You have some amount of
ingredients and your goal is to maximize profit. So you should find such combination of different cakes, which you can
make with your amount of supplies and raise maximum amount of money to donate it to charity organization.

.. image:: ../../_static/img/guides/max_min/cakes/cupcakes.jpg
  :width: 600
  :alt: Cupcakes (Source: https://www.freepik.com/lifeforstock )

Python Model
------------

.. testcode::

    from collections import namedtuple
    import zython as zn


    class ProfitMaximizer(zn.Model):
        def __init__(self, recipes, available):
            self.cakes = zn.Array(zn.var(int), shape=len(recipes))
            self.constraints = [sum(recipe[i] * cake for recipe, cake in zip(recipes, self.cakes)) <= available[i]
                                for i in range(len(available))]
            self.constraints += [cake >= 0 for cake in self.cakes]


    recipe = namedtuple("recipe", ("flour", "banana", "sugar", "butter", "cocoa"))
    recipes = ((recipe(250, 2, 75, 100, 0), recipe(200, 0, 150, 150, 75)),
               (recipe(250, 2, 75, 100, 0), recipe(200, 0, 150, 150, 75), recipe(300, 1, 100, 100, 30))
               )
    prices = ((400, 450),
              (500, 400, 450))
    available = (recipe(4000, 6, 2000, 500, 500),
                 recipe(100000, 600, 250000, 50000, 75000))
    for r, p, a in zip(recipes, prices, available):
        model = ProfitMaximizer(r, a)
        result = model.solve_maximize(sum(cake * price for cake, price in zip(model.cakes, p)))
        print(result)

.. testoutput::

    Solution(objective=1700, cakes=[2, 2])
    Solution(objective=200000, cakes=[288, 140, 0])
