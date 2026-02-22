import zython as zn
from zython._compile.zinc.to_str import to_str


a1 = zn.Array(zn.var(range(5)), shape=(5,))
a1._name = "a1"
a2 = zn.Array(zn.var(range(5)), shape=(3,))
a2._name = "a2"
a = to_str(zn.forall(a1, a2, lambda x, y: x + y < 5))
print(a)
