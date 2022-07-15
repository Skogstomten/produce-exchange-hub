"""Api models for contacts."""
from datetime import datetime, tzinfo

from pydantic import BaseModel, Field
from bson.objectid import ObjectId
from fastapi import Request
from pytz import utc

from app.utils.datetime_utils import to_timezone
from .base_out_model import BaseOutModel
from ..database_models.contact import ContactDatabaseModel
from ..database_models.user import User
from ..shared import ContactType
from app.utils.request_utils import get_current_request_url_with_additions


class BaseContactModel(BaseModel):
    """Base contact model."""

    type: ContactType
    value: str
    description: str | None = Field(None)


class CreateContactModel(BaseContactModel):
    """Model used for creating a contact."""

    def to_database_model(self, user: User) -> ContactDatabaseModel:
        """Converts model to database model."""
        return ContactDatabaseModel(
            id=str(ObjectId()),
            type=self.type,
            value=self.value,
            description=self.description,
            created_by=user.email,
            created_at=datetime.now(utc),
            changed_by=None,
            changed_at=None,
        )


class UpdateContactModel(BaseContactModel):
    def to_database_model(self, contact_id: str) -> ContactDatabaseModel:
        return ContactDatabaseModel(
            id=contact_id,
            type=self.type,
            value=self.value,
            description=self.description,
        )


class ContactListModel(BaseContactModel, BaseOutModel):
    """Model used when listing contacts."""

    id: str
    created_by: str
    created_at: datetime
    changed_by: str | None
    changed_at: datetime | None

    @classmethod
    def from_database_model(cls, model: ContactDatabaseModel, request: Request, tz: str | tzinfo):
        """Creates model instance from database model."""
        return cls(
            id=model.id,
            type=model.type,
            value=model.value,
            description=model.description,
            created_by=model.created_by,
            created_at=to_timezone(model.created_at, tz),
            changed_by=model.changed_by,
            changed_at=to_timezone(model.changed_at, tz),
            operations=[],
            url=get_current_request_url_with_additions(request, (model.id,)),
        )


class ContactOutModel(ContactListModel, BaseOutModel):
    """Model used when getting a single contact."""
