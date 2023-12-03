from enum import Enum
from typing import TypeVar, Generic

from peewee import Field

T = TypeVar("T", bound=Enum)


class EnumField(Field, Generic[T]):
    field_type = "varchar"

    def __init__(self, enum_type: Enum, **kwargs):
        self.enum_type = enum_type
        super().__init__(**kwargs)

    def db_value(self, value: Enum) -> str:
        return value.value

    def python_value(self, value: str) -> Enum:
        return self.enum_type[value]
