from dbtogo.dbmodel import DBEngineFactory, DBModel


class SimpleDuck(DBModel):
    pk: int = None
    name: str

    @classmethod
    def bind(cls, engine):
        super().bind(engine, "pk", table="test_identity")


def test_identity():
    engine = DBEngineFactory.create_sqlite3_engine("test.db")

    SimpleDuck.bind(engine)
    duck = SimpleDuck(name="McDuck")
    duck.save()

    print(duck._cache)

    duck2 = SimpleDuck.get(name="McDuck")

    print(duck2._cache)

    assert duck.pk == duck2.pk

    print(duck is duck)
    print(duck is duck2)

    duck.delete()


test_identity()
