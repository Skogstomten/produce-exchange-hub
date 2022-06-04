from pydantic import BaseModel

from ..shared import ContactType


class ContactDatabaseModel(BaseModel):
    id: str
    type: ContactType
    value: str
    description: str | None
