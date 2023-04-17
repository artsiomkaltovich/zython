Inventory
=========

Let's solve some variant of the tiling problem:

* given field with specified size
* and some objects (tiles) as rectangles with specified width and length
* find a way to put all such tiles in the field without overlaps.

This is similar to how inventory works in some old-fashioned RPG.

In our model we define field as ``M*N`` matrix `A`, where:

* `A[i, j] == -1` means the cell is empty (contains no tile)
* `A[i, j] == 0` just means, that cell's value isn't calculated yet.
* `A[i, j] == K` - means the cell is occupied by tile with the number of `K`.

We will use ``zn.exists`` function for the model definition, basically we will say that for every object(tile) the
should exist at least one region in the field with the size of the object and its value.

Python Model
------------

.. testcode::

    import zython as zn


    class MyModel(zn.Model):
        def __init__(self, objects, inventory_shape):
            self.objects = zn.Array(objects)
            self.inventory = zn.Array(zn.var(zn.range(-1, self.objects.size(0))), shape=inventory_shape)
            self.constraints = [zn.forall(zn.range(self.objects.size(0)), self.obj_exists())]

        def obj_exists(self):
            """ constraints every object exists in the field """
            # Just iterate through every possible position and constraint there should be object in the field
            inventory = self.inventory
            return lambda obj: zn.exists(zn.range(inventory.size(0) - self.objects[obj, 0] + 1),
                                         lambda i: zn.exists(zn.range(inventory.size(1) - self.objects[obj, 1] + 1),
                                                             lambda j: self.iter_obj(i, j, obj)))

        def iter_obj(self, i, j, obj_idx):
            """ constraints every cell of object is filled with the same number """
            return zn.forall(zn.range(self.objects[obj_idx, 0]),
                             lambda k1: zn.forall(zn.range(self.objects[obj_idx, 1]),
                                                  lambda k2: self.inventory[i + k1, j + k2] == obj_idx))


    # functions to check result correctness
    def check(r, objects):
        for obj, (height, width) in enumerate(objects):
            find_obj(r, obj, width, height)


    def find_obj(r, obj, width, height):
        for i in range(len(r)):
            for j in range(len(r[0])):
                if r[i][j] == obj:
                    for h in range(1, height):
                        for w in range(1, width):
                            assert r[i + h][j + w] == obj
                    return
        raise AssertionError("obj {} not found".format(obj))


    objects1 = [[1, 2], [2, 1], [4, 1], [2, 2]]
    shape1 = (5, 4)
    objects2 = [[1, 2], [2, 1], [4, 1], [2, 2]]
    shape2 = (5, 4)
    for objects, shape in zip((objects1, objects2), (shape1, shape2)):
        model = MyModel(objects, shape)
        result = model.solve_satisfy()
        r = result["inventory"]
        check(r, objects)
    print("all checks pass")

.. testoutput::

    all checks pass


.. warning::

    ``zn.exists`` doesn't mean there will be one and only one such tile, it just constrain there will be *at least* one.

Solutions
---------

We run the model for 2 cases: and it returns the following fields:

* (5x4) field with 4 objects:

.. image:: ../../_static/img/guides/array_advanced/inventory/inventory1.png
  :width: 300
  :alt: Inventory 1

* (3x3) field with 3 objects:

.. image:: ../../_static/img/guides/array_advanced/inventory/inventory2.png
  :width: 225
  :alt: Inventory 2
