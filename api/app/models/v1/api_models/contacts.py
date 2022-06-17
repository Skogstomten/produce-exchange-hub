"""Api models for contacts."""
from pydantic import BaseModel, Field
from bson.objectid import ObjectId
from fastapi import Request

from .base_out_model import BaseOutModel
from ..database_models.contact_database_model import ContactDatabaseModel
from ..shared import ContactType
from app.utils.request_utils import get_current_request_url_with_additions


class CreateContactModel(BaseModel):
    """Model used for creating a contact."""
    type: ContactType
    value: str
    description: str | None = Field(None)

    def to_database_model(self) -> ContactDatabaseModel:
        """Converts model to database model."""
        return ContactDatabaseModel(
            id=str(ObjectId()),
            type=self.type.value,
            value=self.value,
            description=self.description,
        )


class ContactListModel(CreateContactModel):
    """Model used when listing contacts."""
    id: str


class ContactOutModel(ContactListModel, BaseOutModel):
    """Model used when getting a single contact."""
    @classmethod
    def from_database_model(
        cls, model: ContactDatabaseModel, request: Request
    ):
        """Creates model instance from database model."""
        return cls(
            **model.dict(),
            operations=[],
            url=get_current_request_url_with_additions(request, (model.id,))
        )
