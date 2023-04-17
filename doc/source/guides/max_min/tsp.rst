Travel Salesman Problem
=======================


`Travel Salesman (or salesperson?) Problem <https://en.wikipedia.org/wiki/Travelling_salesman_problem>`_ is a famous
example of minimization problem. It tries to find the answer on the following question:
"Given a list of cities and the distances between each pair of cities,
what is the shortest possible route that visits each city exactly once and returns to the origin city?"

.. image:: ../../_static/img/guides/max_min/tsp/TSP_Deutschland.png
  :width: 300
  :alt: TSP solution for the 15 biggest cities of Germany
    (Source: https://www.cia.gov/cia/publications/factbook/maps/gm-map.gif )

Python Model
------------

.. testcode::

    import zython as zn


    class TSP(zn.Model):
        def __init__(self, distances):
            self.distances = zn.Array(distances)
            self.path = zn.Array(zn.var(range(len(distances))), shape=len(distances))
            self.cost = (zn.sum(range(1, len(distances)), lambda i: self.distances[self.path[i - 1], self.path[i]])
                         + self.distances[self.path[len(distances) - 1], self.path[0]])
            self.constraints = [zn.circuit(self.path)]


    distances = [[0, 6, 4, 5, 8], [6, 0, 4, 7, 6], [4, 4, 0, 3, 4], [5, 7, 3, 0, 5], [8, 6, 4, 5, 0]]
    model = TSP(distances)
    result = model.solve_minimize(model.cost)
    print(result)

.. testoutput::

    Solution(objective=24, path=[3, 2, 4, 1, 0], cost=24)