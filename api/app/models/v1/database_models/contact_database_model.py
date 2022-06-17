"""ContactDatabaseModel."""
from pydantic import BaseModel


class ContactDatabaseModel(BaseModel):
    """DB model for contacts."""

    id: str
    type: str
    value: str
    description: str | None
