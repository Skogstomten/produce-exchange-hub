from typing import TypeVar, Generic

from peewee import Field

T = TypeVar("T")


class SetField(Field, Generic[T]):
    field_type = "set"

    def db_value(self, value: list[T]) -> str:
        return "|".join(value)

    def python_value(self, value: str) -> list[T]:
        return value.split("|")
