from datetime import datetime

from pydantic import BaseModel, Field

from app.database.document_database import Document
from .contact_database_model import ContactDatabaseModel


class CompanyDatabaseModel(BaseModel):
    id: str
    name: dict[str, str]
    status: str
    created_date: datetime
    company_types: list[str]
    content_languages_iso: list[str]
    activation_date: datetime | None
    description: dict[str, str]
    contacts: list[ContactDatabaseModel] | None = Field(None)
    authorized_users: dict[str, str] = Field([])
