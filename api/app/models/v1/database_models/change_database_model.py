from datetime import datetime
from enum import Enum

from bson import ObjectId
from pydantic import BaseModel
from pytz import utc


class ChangeType(Enum):
    """Enum containing change types for change model."""

    add = "add"
    update = "update"
    delete = "delete"


class ChangeDatabaseModel(BaseModel):
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
        path: str,
        change_type: ChangeType,
        username: str,
        new_value: str | int | float | datetime | dict | list | Enum | None,
    ):
        """Creates a new instance of ChangeDatabaseModel."""
        return cls(
            id=str(ObjectId()),
            path=path,
            change_type=change_type,
            actor_username=username,
            changed_at=datetime.now(utc),
            new_value=new_value,
        )
