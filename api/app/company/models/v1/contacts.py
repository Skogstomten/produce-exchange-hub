"""Api models for contacts."""
from datetime import datetime, tzinfo

from fastapi import Request
from pydantic import BaseModel, Field

from app.company.models.db.contact import Contact
from app.company.models.shared.enums import ContactType
from app.company.utils.datetime_utils import to_timezone
from app.shared.models.v1.base_out_model import BaseOutModel
from app.shared.utils.request_utils import get_current_request_url_with_additions


class BaseContactModel(BaseModel):
    """Base contact model."""

    type: ContactType
    value: str
    description: str | None = Field(None)


class AddContactModel(BaseContactModel):
    """Model used for creating a contact."""


class UpdateContactModel(BaseContactModel):
    pass


class ContactListModel(BaseContactModel, BaseOutModel):
    """Model used when listing contacts."""

    id: str
    created_by: str
    created_at: datetime
    changed_by: str | None
    changed_at: datetime | None

    @classmethod
    def from_database_model(cls, model: Contact, request: Request, tz: str | tzinfo):
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
