"""CompanyDatabaseModel"""
from datetime import datetime
from enum import Enum

from bson import ObjectId
from pydantic import BaseModel, Field
from pytz import utc

from .contact_database_model import ContactDatabaseModel


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
    actor_id: str
    actor_username: str
    changed_at: datetime

    @classmethod
    def create(cls, path: str, change_type: ChangeType, user_id: str, username: str):
        """Creates a new instance of ChangeDatabaseModel."""
        return cls(
            id=str(ObjectId()),
            path=path,
            change_type=change_type,
            actor_id=user_id,
            actor_username=username,
            changed_at=datetime.now(utc),
        )


class CompanyDatabaseModel(BaseModel):
    """DB model for companies."""

    id: str
    name: dict[str, str]
    status: str
    created_date: datetime
    company_types: list[str]
    content_languages_iso: list[str]
    activation_date: datetime | None
    description: dict[str, str]
    external_website_url: str | None
    contacts: list[ContactDatabaseModel] | None = Field([])
    changes: list[ChangeDatabaseModel] = Field([])
