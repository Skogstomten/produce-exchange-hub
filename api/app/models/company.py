from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class CompanyTypes(Enum):
    producer = 'producer'
    buyer = 'buyer'


class CompanyIn(BaseModel):
    name: dict[str, str]
    company_types: list[CompanyTypes] = Field(..., min_items=1)
    content_languages_iso: list[str] = Field(..., min_length=2, max_length=2, min_items=1)


class CompanyPublic(BaseModel):
    id: str
    name: dict[str, str]
    status: str
    created_date: datetime
    company_types: list[str]
    content_languages_iso: list[str]
    activation_date: datetime | None

