"""ContactDatabaseModel."""
from datetime import datetime

from pydantic import BaseModel, Field
from pytz import utc

from app.authentication.models.db.user import User
from app.company.models.shared.enums import ContactType


class Contact(BaseModel):
    """DB model for contacts."""

    id: str
    type: ContactType
    value: str
    description: str | None
    created_by: str = Field("MISSING")
    created_at: datetime = Field(datetime.now(utc))
    changed_by: str | None
    changed_at: datetime | None

    @classmethod
    def from_create_contract_model(cls, new_contact_id: str, model_dict: dict, authenticated_user: User):
        return cls(
            id=new_contact_id,
            created_by=authenticated_user.email,
            **model_dict,
        )
