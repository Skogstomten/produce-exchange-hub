from enum import Enum, unique
from datetime import datetime
import pytz

from pydantic import BaseModel, Field
from fastapi import Request

from .base_out_model import BaseOutModel
from ..shared import CompanyStatus, Language, ContactType
from ..database_models.companies import CompanyDatabaseModel
from app.utils.lang_utils import select_localized_text
from app.utils.datetime_utils import ensure_utc


@unique
class CompanyTypes(Enum):
    producer = 'producer'
    buyer = 'buyer'


class ContactOutModel(BaseModel):
    id: str
    type: ContactType
    value: str
    description: str | None


class CompanyOutModel(BaseOutModel):
    id: str
    name: str
    status: CompanyStatus
    created_date: datetime
    company_types: list[str]
    content_languages_iso: list[str]
    activation_date: datetime | None
    description: str | None = Field(None)
    contacts: list[ContactOutModel] | None

    @classmethod
    def from_database_model(
            cls,
            model: CompanyDatabaseModel,
            lang: Language,
            timezone: str,
            request: Request,
            include_contacts: bool,
    ):
        operations = []

        activation_date = model.activation_date
        if activation_date is not None:
            activation_date = ensure_utc(activation_date).astimezone(pytz.timezone(timezone))

        return cls(
            url=str(request.url),
            operations=operations,

            id=model.id,
            name=select_localized_text(model.name, lang, model.content_languages_iso),
            status=model.status,
            created_date=ensure_utc(model.created_date).astimezone(pytz.timezone(timezone)),
            company_types=model.company_types,
            content_languages_iso=model.content_languages_iso,
            activation_date=activation_date,
            description=select_localized_text(model.description, lang, model.content_languages_iso),

            contacts=model.contacts if include_contacts else None,
        )


class CompanyCreateModel(BaseModel):
    name: dict[str, str]
    company_types: list[CompanyTypes] = Field(..., min_items=1)
    content_languages_iso: list[str] = Field(..., min_length=2, max_length=2, min_items=1)

    def to_database_model(self) -> CompanyDatabaseModel:
        return CompanyDatabaseModel(
            name=self.name,
            status=CompanyStatus.created,
            created_date=datetime.now(pytz.UTC),
            company_types=self.company_types,
            content_languages_iso=self.content_languages_iso,
            description={}
        )


class CompanyUpdateModel(BaseModel):
    name: dict[str, str]
    status: CompanyStatus = Field(...)
    company_types: list[CompanyTypes] = Field(..., min_items=1)
    content_languages_iso: list[str] = Field(..., min_length=2, max_length=2, min_items=1)
    description: dict[str, str] = Field({})

    def to_database_model(self, company_id: str):
        return CompanyDatabaseModel(
            id=company_id,
            name=self.name,
            status=self.status,
            company_types=self.company_types,
            content_languages_iso=self.content_languages_iso,
            description=self.description
        )
