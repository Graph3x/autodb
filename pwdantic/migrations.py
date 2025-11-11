from pwdantic.serialization import SQLColumn


Migration = list["MigrationStep"]


class InvalidMigrationError(Exception):
    pass


class MigrationStep:
    destructive: bool


class AddCol(MigrationStep):
    name: str


class DropCol(MigrationStep):
    name: str
    destructive: bool = True


class Rename(MigrationStep):
    old_name: str
    new_name: str


class Retype(MigrationStep):
    column: str
    old_type: str
    new_type: str
    destructive: bool = True


class AddConstraint(MigrationStep):
    column: str
    constraint: str


class RemoveConstraint(MigrationStep):
    column: str
    constraint: str


class MigrationEngine:
    def generate_migration(
        self, original: list[SQLColumn], new: list[SQLColumn]
    ) -> Migration:
        pass
