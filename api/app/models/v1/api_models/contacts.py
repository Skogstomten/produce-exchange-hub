from pydantic import BaseModel, Field
from bson.objectid import ObjectId
from fastapi import Request

from .base_out_model import BaseOutModel
from ..database_models.contact_database_model import ContactDatabaseModel
from ..shared import ContactType
from app.utils.request_utils import get_current_request_url_with_additions


class CreateContactModel(BaseModel):
    type: ContactType
    value: str
    description: str | None = Field(None)

    def to_database_model(self) -> ContactDatabaseModel:
        return ContactDatabaseModel(
            id=str(ObjectId()),
            type=self.type.value,
            value=self.value,
            description=self.description,
        )


class ContactListModel(CreateContactModel):
    id: str


class ContactOutModel(ContactListModel, BaseOutModel):
    @classmethod
    def from_database_model(
        cls, model: ContactDatabaseModel, request: Request
    ):
        return cls(
            **model.dict(),
            operations=[],
            url=get_current_request_url_with_additions(request, (model.id,))
        )
