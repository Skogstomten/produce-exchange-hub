"""ContactDatabaseModel."""
from datetime import datetime

from pydantic import BaseModel, Field
from pytz import utc

from app.shared.models.v1.shared import ContactType


class ContactDatabaseModel(BaseModel):
    """DB model for contacts."""

    id: str
    type: ContactType
    value: str
    description: str | None
    created_by: str = Field("MISSING")
    created_at: datetime = Field(datetime.now(utc))
    changed_by: str | None
    changed_at: datetime | None
