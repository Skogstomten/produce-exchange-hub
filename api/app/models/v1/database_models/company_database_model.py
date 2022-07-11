"""CompanyDatabaseModel"""
from datetime import datetime

from pydantic import BaseModel, Field

from .change_database_model import ChangeDatabaseModel
from .contact_database_model import ContactDatabaseModel
from ..shared import CompanyStatus


class CompanyDatabaseModel(BaseModel):
    """DB model for companies."""

    id: str
    name: dict[str, str]
    status: CompanyStatus
    created_date: datetime
    company_types: list[str]
    content_languages_iso: list[str]
    activation_date: datetime | None
    description: dict[str, str]
    external_website_url: str | None
    profile_picture_url: str | None
    contacts: list[ContactDatabaseModel] | None = Field([])
    changes: list[ChangeDatabaseModel] = Field([])
