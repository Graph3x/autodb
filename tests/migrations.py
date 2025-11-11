from pwdantic.pwdantic import PWModel, PWEngineFactory, PWEngine
from pwdantic.migrations import *
from pwdantic.datatypes import SQLType, SQLColumn


class MigrationTestModelOld(PWModel):
    pk: int | None = None
    unq_string: str
    nullable_int: int | None = None

    @classmethod
    def bind(cls, engine):
        super().bind(
            engine,
            primary_key="pk",
            unique=["unq_string"],
            table="migration_test",
        )


class MigrationTestModelNew(PWModel):
    pk: int | None = None
    unq_string: str
    the_same_int: int | None = None
    new_col: str | None = "default"

    @classmethod
    def bind(cls, engine):
        super().bind(
            engine,
            primary_key="unq_string",
            unique=["pk"],
            table="migration_test",
        )


def test_migrations(engine: PWEngine):
    MigrationTestModelOld.bind(engine)
    MigrationTestModelNew.bind(engine)


def manual_migration(engine: PWEngine):
    MigrationTestModelOld.bind(engine)

    migration = [
        AddCol(SQLColumn("new_col", SQLType.string, True, "default"))
    ]

    engine.migrate()


def main():
    engine = PWEngineFactory.create_sqlite3_engine("test.db")
    # test_migrations(engine)
    manual_migration(engine)


if __name__ == "__main__":
    main()
