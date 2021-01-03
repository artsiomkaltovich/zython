Inventory
=========


Python Model
------------

.. testcode::

    import zython as zn


    class MyModel(zn.Model):
        def __init__(self, objects, inventory_shape):
            self.objects = zn.Array(objects)
            self.inventory = zn.Array(zn.var(range(-1, self.objects.size(0))), shape=inventory_shape)
            self.constraints = [zn.forall(range(self.objects.size(0)), self.obj_exists())]

        def obj_exists(self):
            inventory = self.inventory
            return lambda obj: zn.exists(range(inventory.size(0) - self.objects[obj, 0] + 1),
                                         lambda i: zn.exists(range(inventory.size(1) - self.objects[obj, 1] + 1),
                                                             lambda j: self.iter_obj(i, j, obj)))

        def iter_obj(self, i, j, obj_idx):
            return zn.forall(range(self.objects[obj_idx, 0]),
                             lambda k1: zn.forall(range(self.objects[obj_idx, 1]),
                                                  lambda k2: self.inventory[i + k1, j + k2] == obj_idx))


    model = MyModel([[1, 2], [2, 1], [4, 1], [2, 2]], (5, 4))
    result = model.solve_satisfy()
    print(result["inventory"])

    model = MyModel([[1, 2], [2, 2], [3, 1]], (3, 3))
    result = model.solve_satisfy()
    print(result["inventory"])

.. testoutput::

    [[2, 1, 3, 3], [2, 1, 3, 3], [2, 0, 0, -1], [2, -1, -1, -1], [-1, -1, -1, -1]]
    [[2, 0, 0], [2, 1, 1], [2, 1, 1]]
