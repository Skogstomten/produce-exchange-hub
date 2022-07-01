"""Api models for contacts."""
from datetime import datetime

from pydantic import BaseModel, Field
from bson.objectid import ObjectId
from fastapi import Request
from pytz import utc

from .base_out_model import BaseOutModel
from ..database_models.contact_database_model import ContactDatabaseModel
from ..database_models.user_database_model import UserDatabaseModel
from ..shared import ContactType
from app.utils.request_utils import get_current_request_url_with_additions


class CreateContactModel(BaseModel):
    """Model used for creating a contact."""

    type: ContactType
    value: str
    description: str | None = Field(None)

    def to_database_model(self, user: UserDatabaseModel) -> ContactDatabaseModel:
        """Converts model to database model."""
        return ContactDatabaseModel(
            id=str(ObjectId()),
            type=self.type.value,
            value=self.value,
            description=self.description,
            created_by=user.email,
            created_at=datetime.now(utc),
        )


class ContactListModel(CreateContactModel):
    """Model used when listing contacts."""

    id: str


class ContactOutModel(ContactListModel, BaseOutModel):
    """Model used when getting a single contact."""

    @classmethod
    def from_database_model(cls, model: ContactDatabaseModel, request: Request):
        """Creates model instance from database model."""
        return cls(**model.dict(), operations=[], url=get_current_request_url_with_additions(request, (model.id,)))
