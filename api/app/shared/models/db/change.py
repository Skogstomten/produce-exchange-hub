from datetime import datetime
from enum import Enum

from pydantic import BaseModel
from pytz import utc


class ChangeType(Enum):
    """Enum containing change types for change model."""

    add = "add"
    update = "update"
    delete = "delete"


class Change(BaseModel):
    """Database model for changes."""

    id: str
    path: str
    change_type: ChangeType
    actor_username: str
    changed_at: datetime
    new_value: str | int | float | datetime | dict | list | Enum | None

    @classmethod
    def create(
        cls,
        change_id: str,
        path: str,
        change_type: ChangeType,
        username: str,
        new_value: str | int | float | datetime | dict | list | Enum | None,
    ) -> "Change":
        """
        Creates a new instance of ChangeDatabaseModel.
        :param change_id: The id to use for the change. Should be a generated id supported by the underlying database.
        :param path: Path of changed field.
        :param change_type: Type of change.
        :param username: Username of user instigating the change.
        :param new_value: The new value.
        """
        return cls(
            id=change_id,
            path=path,
            change_type=change_type,
            actor_username=username,
            changed_at=datetime.now(utc),
            new_value=new_value,
        )
