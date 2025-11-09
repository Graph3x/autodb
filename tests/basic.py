from pwdantic.pwdantic import PWModel, PWEngineFactory




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
    print(Duck.get(name="McDuck"))

    mc_duck = Duck(name="McDuck", color="Yellow", age=42)
    mc_duck.save()


if __name__ == "__main__":
    main()
