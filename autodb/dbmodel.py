from pydantic import BaseModel
import abc
import sqlite3
from typing import Self

from autodb.exceptions import *
from autodb.sqlite import SqliteEngine
from autodb.datatypes import DBEngine, SQLColumn

from autodb.serialization import GeneralSQLSerializer

DEFAULT_PRIM_KEYS = ["id", "primary_key", "uuid"]


class DBEngineFactory(abc.ABC):
    @staticmethod
    def create_sqlite3_engine(database: str = "") -> DBEngine:
        conn = sqlite3.connect(database)
        return SqliteEngine(conn)


def bound(func):
    def wrapper(cls, *args, **kwargs):
        if "db" not in dir(cls):
            raise NoBindError()

        return func(cls, *args, **kwargs)

    return wrapper


class DBModel(BaseModel):
    @classmethod
    def bind(
        cls,
        db: DBEngine,
        primary_key: str | None = None,
        unique: list[str] = [],
        table: str = None,
    ):
        cls.db = db
        table = table if table is not None else cls.__name__

        columns = GeneralSQLSerializer().serialize_schema(
            cls.__name__, cls.model_json_schema(), primary_key, unique
        )

        used_names = [x.name for x in columns]
        if primary_key is None:
            for prim in DEFAULT_PRIM_KEYS:
                if prim in used_names:
                    continue
                primary_key = prim
                columns.append(SQLColumn(prim, int, False, None, True, True))

        cls._primary = primary_key
        cls.table = table
        db.migrate(table, columns)

    @classmethod
    def _deserialize_object(cls, object_data: dict) -> Self:
        object = GeneralSQLSerializer().deserialize_object(cls, object_data)

        pk = getattr(object, object.__class__._primary)
        setattr(object, "_data_bind", pk)

        return object

    @classmethod
    @bound
    def get(cls, **kwargs) -> Self:
        data = cls.db.select("*", cls.table, kwargs)

        if len(data) < 1:
            return None

        return cls._deserialize_object(data[0])

    def _create(self):
        obj_data = GeneralSQLSerializer().serialize_object(self)

        insert_bind = self.db.insert(self.__class__.table, obj_data)
        bind_attr = getattr(self, self.__class__._primary)

        data_bind = bind_attr if bind_attr != None else insert_bind
        setattr(self, "_data_bind", data_bind)

    def _update(self):
        bind = self._data_bind

        if getattr(self, self.__class__._primary) != bind:
            raise BindViolationError()

        obj_data = GeneralSQLSerializer().serialize_object(self)
        self.db.update(
            self.__class__.table, obj_data, self.__class__._primary
        )

    @bound
    def save(self):
        if getattr(self, "_data_bind", None) is None:
            return self._create()
        return self._update()

    @bound
    def delete(self):
        if getattr(self, "_data_bind", None) is None:
            raise UnboundDeleteError()

        primary_key = self.__class__._primary
        primary_value = self._data_bind

        self.db.delete(self.__class__.table, primary_key, primary_value)
        self._data_bind = None

    @classmethod
    @bound
    def all(cls) -> list[Self]:
        data = cls.db.select("*", cls.table)
        return [cls._deserialize_object(x) for x in data]
