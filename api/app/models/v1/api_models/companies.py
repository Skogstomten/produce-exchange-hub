"""API model classes for companies."""
from datetime import datetime, tzinfo
from enum import Enum, unique

from fastapi import Request
from pydantic import BaseModel, Field

from app.utils.datetime_utils import to_timezone
from app.utils.lang_utils import select_localized_text
from app.utils.request_utils import get_current_request_url_with_additions
from .base_out_model import BaseOutModel
from .contacts import ContactListModel
from ..database_models.company_database_model import CompanyDatabaseModel
from ..shared import CompanyStatus, Language


@unique
class CompanyTypes(Enum):
    """Enum with the available company types."""

    producer = "producer"
    buyer = "buyer"


def _initialize_company_model(
    cls,
    model: CompanyDatabaseModel,
    lang: Language,
    tz: str | tzinfo,
    request: Request,
):
    instance = cls(
        url=get_current_request_url_with_additions(request),
        operations=[],
        id=model.id,
        name=select_localized_text(model.name, lang, model.content_languages_iso),
        status=model.status,
        created_date=to_timezone(model.created_date, tz),
        company_types=model.company_types,
        content_languages_iso=model.content_languages_iso,
        activation_date=to_timezone(model.activation_date, tz),
        description=select_localized_text(model.description, lang, model.content_languages_iso),
        external_website_url=model.external_website_url,
        profile_picture_url=model.profile_picture_url,
    )
    if isinstance(cls, CompanyOutModel):
        instance.contacts = model.contacts

    return instance


class CompanyOutListModel(BaseOutModel):
    """Company model used when listing companies."""

    id: str
    name: str
    status: CompanyStatus
    created_date: datetime
    company_types: list[str]
    content_languages_iso: list[str]
    activation_date: datetime | None
    description: str | None = Field(None)
    external_website_url: str | None
    profile_picture_url: str | None

    @classmethod
    def from_database_model(
        cls,
        model: CompanyDatabaseModel,
        lang: Language,
        tz: str | tzinfo,
        request: Request,
    ):
        """Creates model from database model with localization."""
        return _initialize_company_model(cls, model, lang, tz, request)


class CompanyOutModel(CompanyOutListModel):
    """Company model used when getting a single company."""

    contacts: list[ContactListModel] | None

    @classmethod
    def from_database_model(
        cls,
        model: CompanyDatabaseModel,
        lang: Language,
        tz: str | tzinfo,
        request: Request,
    ):
        """Creates model from database model with localization."""
        return _initialize_company_model(cls, model, lang, tz, request)


class CompanyCreateModel(BaseModel):
    """Model used when creating a new company."""

    name: dict[str, str]
    company_types: list[CompanyTypes] = Field(..., min_items=1)
    content_languages_iso: list[str] = Field(..., min_length=2, max_length=2, min_items=1)
    external_website_url: str | None


class CompanyUpdateModel(BaseModel):
    """Model used when updating company."""

    company_types: list[CompanyTypes] = Field(..., min_items=1)
    content_languages_iso: list[str] = Field(..., min_length=2, max_length=2, min_items=1)
    external_website_url: str | None
