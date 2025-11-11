import abc
from typing import Any


Migration = list["MigrationStep"]


class SQLColumn:
    def __init__(
        self,
        name: str,
        datatype: str,
        nullable: bool,
        default: Any,
        primary: bool = False,
        unique: bool = False,
    ):
        self.name: str = name
        self.datatype: str = datatype
        self.nullable: bool = nullable
        self.default: Any = default
        self.primary_key: bool = primary
        self.unique: bool = unique

    def __str__(self):
        return f"{self.name}: {("nullable " if self.nullable else "")}{("unique " if self.unique else "")}{("primary " if self.primary_key else "")}{self.datatype} ({self.default})"


class InvalidMigrationError(Exception):
    pass


class MigrationStep:
    desctructive: bool = False


class DesctructiveMigrationStep(MigrationStep):
    desctructive: bool = True


class AddCol(MigrationStep):
    def __init__(self, column: SQLColumn):
        self.column = SQLColumn


class DropCol(DesctructiveMigrationStep):
    def __init__(self, column_name: str):
        self.column_name = column_name


class RenameCol(MigrationStep):
    def __init__(self, old_name: str, new_name: str):
        self.old_name = old_name
        self.new_name = new_name


class RetypeCol(DesctructiveMigrationStep):
    def __init__(self, column_name: str, old_type: str, new_type: str):
        self.column_name = column_name
        self.old_type = old_type
        self.new_type = new_type


class AddConstraint(MigrationStep):
    def __init__(self, column_name: str, constraint: str):
        self.column_name = column_name
        self.constraint = constraint


class RemoveConstraint(MigrationStep):
    def __init__(self, column_name: str, constraint: str):
        self.column_name = column_name
        self.constraint = constraint


class PWEngine(abc.ABC):

    def select(
        self, field: str, table: str, conditions: dict[str, Any] | None = None
    ) -> list[Any]:
        pass

    def insert(self, table: str, data: list[tuple]):
        pass

    def migrate(self, table: str, columns: list[SQLColumn]):
        pass

    def update(self, table: str, obj_data: dict[str, Any], primary_key: str):
        pass

    def delete(self, table: str, key: str, value: Any):
        pass

    def execute_migration(self, migration: Migration, force: bool = False):
        pass


class SQLType:
    integer = "integer"
    date_time = "date-time"
    string = "string"
    number = "number"
    boolean = "boolean"
    byte_data = "bytes"
