from pwdantic.pwdantic import PWModel, PWEngineFactory


def exp():
    class Duck(PWModel):
        id: int | None = None
        name: str
        color: str = "Brown"
        age: int | None = None
        children: list["Duck"] = []

    for k, v in Duck.model_json_schema().items():
        print(k)
        print(v)
        print()


def main():
    engine = PWEngineFactory.create_sqlite3_engine("test.db")

    class Duck(PWModel):
        id: int | None = None
        name: str
        color: str = "Brown"
        age: int | None = None

        @classmethod
        def bind(cls, engine):
            super().bind(engine, primary_key="id", unique=["name"])

    Duck.bind(engine)

    mc_duck = Duck(name="McDuck", color="Yellow", age=42)
    mc_duck.save()

    print(Duck.get(name="McDuck"))

    mc_duck_junior = Duck(name="Junior", age=15)
    mc_duck_junior.save()

    print(Duck.get(name="McDuck"))


if __name__ == "__main__":
    exp()
    # main()
