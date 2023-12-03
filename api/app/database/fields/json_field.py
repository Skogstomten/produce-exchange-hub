import json
from typing import TypeVar, Generic

from peewee import Field

T = TypeVar("T")


class JsonField(Field, Generic[T]):
    field_type = "text"

    def db_value(self, value: T) -> str:
        return json.dumps(value)

    def python_value(self, value: str) -> T:
        return json.loads(value)
