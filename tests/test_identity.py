from dbtogo.dbmodel import DBEngineFactory, DBModel


class SimpleDuck(DBModel):
    pk: int = None
    name: str

    @classmethod
    def bind(cls, engine):
        super().bind(engine, "pk", table="test_identity")


def dont_test_identity():
    engine = DBEngineFactory.create_sqlite3_engine("test.db")

    SimpleDuck.bind(engine)
    duck = SimpleDuck(name="Duck")
    duck.save()

    duck2 = SimpleDuck.get(name="Duck")

    print(duck is duck2)
    print(duck.pk == duck2.pk)

    duck.pk = 67

    duck3 = SimpleDuck.get(name="Duck")
    print(duck is duck3)

    duck.save()
    duck4 = SimpleDuck.get(name="Duck")
    print(duck is duck4)

    duck.delete()

    print(SimpleDuck.all())


dont_test_identity()
