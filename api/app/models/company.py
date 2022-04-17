from datetime import datetime
from enum import Enum, unique

from pydantic import BaseModel, Field


@unique
class CompanyTypes(Enum):
    producer = 'producer'
    buyer = 'buyer'


@unique
class CompanyStatus(Enum):
    created = 'created'
    active = 'active'
    deactivated = 'deactivated'


class CompanyCreateModel(BaseModel):
    name: dict[str, str]
    company_types: list[CompanyTypes] = Field(..., min_items=1)
    content_languages_iso: list[str] = Field(..., min_length=2, max_length=2, min_items=1)


class CompanyPublicOutModel(BaseModel):
    id: str
    name: dict[str, str]
    status: CompanyStatus
    created_date: datetime
    company_types: list[str]
    content_languages_iso: list[str]
    activation_date: datetime | None
    description: dict[str, str] = Field(None)


class CompanyUpdateModel(BaseModel):
    name: dict[str, str]
    status: CompanyStatus = Field(...)
    company_types: list[CompanyTypes] = Field(..., min_items=1)
    content_languages_iso: list[str] = Field(..., min_length=2, max_length=2, min_items=1)
    description: dict[str, str] = Field(None)
