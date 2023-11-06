Table
=====

The table constraint is used to specify if one dimensional array
should be equal to any row of a two dimensional array.

Model
-----

We will recreate the example of the choosing dishes model from
`minizinc <https://www.minizinc.org/doc-2.5.4/en/predicates.html#table>`_
documentation.

Python Model
------------

.. testcode::

    import enum
    import zython as zn


    class Food(enum.IntEnum):
        icecream = 1
        banana = 2
        chocolate_cake = 3
        lasagna = 4
        steak = 5
        rice = 6
        chips = 7
        brocolli = 8
        beans = 9


    class Feature(enum.IntEnum):
        name = 0
        energy = 1
        protein = 2
        salt = 3
        fat = 4
        cost = 5


    DD = [
        [Food.icecream.value, 1200, 50, 10, 120, 400],
        [Food.banana.value, 800, 120, 5, 20, 120],
        [Food.chocolate_cake.value, 2500, 400, 20, 100, 600],
        [Food.lasagna.value, 3000, 200, 100, 250, 450],
        [Food.steak.value, 1800, 800, 50, 100, 1200],
        [Food.rice.value, 1200, 50, 5, 20, 100],
        [Food.chips.value, 2000, 50, 200, 200, 250],
        [Food.brocolli.value, 700, 100, 10, 10, 125],
        [Food.beans.value, 1900, 250, 60, 90, 150],
    ]


    class MyModel(zn.Model):
        def __init__(
            self,
            food,
            mains,
            sides,
            desserts,
            dd,
            min_energy,
            min_protein,
            max_salt,
            max_fat,
        ):
            self.food = food
            self.mains = zn.Set(mains)
            self.sides = zn.Set(sides)
            self.desserts = zn.Set(desserts)
            self.dd = zn.Array(dd)
            self.main = zn.Array(zn.var(int), shape=len(Feature))
            self.side = zn.Array(zn.var(int), shape=len(Feature))
            self.dessert = zn.Array(zn.var(int), shape=len(Feature))
            self.budget = zn.var(int)

            self.constraints = [
                self.mains.contains(self.main[Feature.name]),
                self.sides.contains(self.side[Feature.name]),
                self.desserts.contains(self.dessert[Feature.name]),
                self.main[Feature.energy] + self.side[Feature.energy] + self.dessert[Feature.energy] >= min_energy,
                self.main[Feature.protein] + self.side[Feature.protein] + self.dessert[Feature.protein] >= min_protein,
                self.main[Feature.salt] + self.side[Feature.salt] + self.dessert[Feature.salt] <= max_salt,
                self.main[Feature.fat] + self.side[Feature.fat] + self.dessert[Feature.fat] <= max_fat,
                self.budget == self.main[Feature.cost] + self.side[Feature.cost] + self.dessert[Feature.cost],

                zn.table(self.main, self.dd),
                zn.table(self.side, self.dd),
                zn.table(self.dessert, self.dd),
            ]


    model = MyModel(
        Food,
        mains={Food.lasagna, Food.steak, Food.rice},
        sides={Food.chips, Food.brocolli, Food.beans},
        desserts={Food.icecream, Food.banana, Food.chocolate_cake},
        dd=DD,
        min_energy=3300,
        min_protein=500,
        max_salt=180,
        max_fat=320,
    )
    result = model.solve_minimize(model.budget)
    menu = [Food(result[dish][Feature.name]) for dish in ("main", "side", "dessert")]
    print(menu, result["budget"])


.. testoutput::

    [<Food.rice: 6>, <Food.brocolli: 8>, <Food.chocolate_cake: 3>] 825
