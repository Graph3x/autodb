from pwdantic.serialization import SQLColumn
from pwdantic.datatypes import *



class MigrationEngine:
    def generate_migration(
        self, original: list[SQLColumn], new: list[SQLColumn]
    ) -> Migration:
        pass
