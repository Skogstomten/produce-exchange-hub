"""CompanyDatabaseModel"""
from datetime import datetime

from pydantic import BaseModel, Field

from app.shared.models.db.change import Change
from app.shared.models.v1.shared import Language
from .address import Address
from .contact import Contact
from .order import Order
from ..shared.enums import CompanyStatus, CompanyTypes


class Company(BaseModel):
    """DB model for companies."""

    id: str
    name: dict[str, str]
    status: CompanyStatus
    created_date: datetime
    company_types: list[CompanyTypes]
    content_languages_iso: list[Language]
    activation_date: datetime | None
    description: dict[str, str]
    external_website_url: str | None
    profile_picture_url: str | None
    contacts: list[Contact] | None = Field([])
    changes: list[Change] = Field([])
    addresses: list[Address] = Field([])
    orders: list[Order] = Field([])

    @classmethod
    def brief(cls):
        return [
            "name",
            "status",
            "created_date",
            "company_types",
            "content_languages_iso",
            "activation_date",
            "description",
            "external_website_url",
            "profile_picture_url",
        ]
