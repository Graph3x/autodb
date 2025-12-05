import sqlite3
from typing import Any, Self

from pydantic import BaseModel
from pydantic.fields import ModelPrivateAttr

from dbtogo.datatypes import DBEngine, UnboundEngine
from dbtogo.exceptions import NoBindError, UnboundDeleteError
from dbtogo.serialization import GeneralSQLSerializer
from dbtogo.sqlite import SqliteEngine


class DBEngineFactory:
    @staticmethod
    def create_sqlite3_engine(database: str = "") -> DBEngine:
        conn = sqlite3.connect(database)
        return SqliteEngine(conn)


class DBModel(BaseModel):
    _db: DBEngine = UnboundEngine()
    _table: str = "table_not_set"
    _primary: str = "primary_not_set"
    _cache: dict = {}

    @classmethod
    def bind(
        cls,
        db: DBEngine,
        primary_key: str | None = None,
        unique: list[str] = [],
        table: str | None = None,
    ) -> None:
        cls._db = db
        cls._cache = {}

        table = table if table is not None else cls.__name__

        columns = GeneralSQLSerializer().serialize_schema(
            cls.__name__, cls.model_json_schema(), primary_key, unique
        )

        if primary_key is None:
            raise NotImplementedError("Auto primary key is not implemented yet.")

        assert primary_key is not None

        cls._primary = primary_key
        cls._table = table
        db.migrate(table, columns)

    @classmethod
    def _is_bound(cls) -> bool:
        if isinstance(cls._db, UnboundEngine):
            raise NoBindError()

        if isinstance(cls._db, ModelPrivateAttr):
            raise NoBindError()

        return True

    @classmethod
    def _deserialize_object(cls, object_data: tuple) -> Self:
        py_object = GeneralSQLSerializer().deserialize_object(cls, object_data)
        return py_object

    @classmethod
    def get(cls, **kwargs: dict[str, Any]) -> Self | None:
        assert cls._is_bound()

        data = cls._db.select("*", cls._table, kwargs)
        if len(data) < 1:
            return None

        gss = GeneralSQLSerializer()

        new_object_values = gss.partially_deserialize_object(cls, data[0])
        pk_value = new_object_values[cls._primary]

        cached_obj = cls._cache.get(pk_value, None)
        if cached_obj is not None:
            return cached_obj

        return gss.build_object(cls, new_object_values)

    def _create(self) -> None:
        obj_data = GeneralSQLSerializer().serialize_object(self)
        insert_bind = self._db.insert(self.__class__._table, obj_data)

        pk = self.__class__._primary

        if getattr(self, pk) is None:
            setattr(self, pk, insert_bind)

        self.__class__._cache[getattr(self, pk)] = self

    def _update(self) -> None:
        obj_data = GeneralSQLSerializer().serialize_object(self)
        self._db.update(self.__class__._table, obj_data, self.__class__._primary)

    def save(self) -> None:
        assert self.__class__._is_bound()

        pk_value = getattr(self, self.__class__._primary, None)
        if pk_value is None or self.__class__._cache.get(pk_value, None) is None:
            return self._create()

        return self._update()

    def delete(self) -> None:
        assert self.__class__._is_bound()

        pk_value = getattr(self, self.__class__._primary)

        if pk_value is None or self._cache.get(pk_value, None) is None:
            raise UnboundDeleteError()

        self._db.delete(self.__class__._table, self.__class__._primary, pk_value)

    @classmethod
    def all(cls) -> list[Self]:
        assert cls._is_bound()

        data = cls._db.select("*", cls._table)
        return [cls._deserialize_object(x) for x in data]
