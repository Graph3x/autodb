from pwdantic.pwdantic import PWModel, PWEngineFactory, PWEngine


class MigrationTestModelOld(PWModel):
    pk: int | None = None
    unq_string: str
    nullable_int: int | None = None

    @classmethod
    def bind(cls, engine):
        super().bind(engine, primary_key="pk", unique=["unq_string"], table="migration_test")


class MigrationTestModelNew(PWModel):
    pk: int | None = None
    unq_string: str
    nullable_int: int | None = None

    @classmethod
    def bind(cls, engine):
        super().bind(engine, primary_key="pk", unique=["unq_string"], table="migration_test")


def test_migrations(engine: PWEngine):
    MigrationTestModelOld.bind(engine)
    MigrationTestModelNew.bind(engine)


def main():
    engine = PWEngineFactory.create_sqlite3_engine("test.db")
    test_migrations(engine)


if __name__ == "__main__":
    main()
