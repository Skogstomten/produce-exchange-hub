from pydantic import BaseModel

from ..shared import ContactType


class ContactDatabaseModel(BaseModel):
    id: str
    type: str
    value: str
    description: str | None
