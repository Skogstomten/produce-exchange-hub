from pydantic import BaseModel


class ContactDatabaseModel(BaseModel):
    id: str
    type: str
    value: str
    description: str | None
