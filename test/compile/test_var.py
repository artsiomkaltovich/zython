import zython as zn


def test_range_one_arg():
    class MyModel(zn.Model):
        def __init__(self):
            self.a = zn.var(range(100))

    model = MyModel()
    src = model.compile()
    assert "var 0..99: a;" in src
