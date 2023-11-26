"""API model classes for companies."""
from datetime import datetime, tzinfo
from typing import List
from uuid import UUID

from fastapi import Request, APIRouter
from pydantic import BaseModel, Field

from app.authentication.models.db.user import User
from app.company.models.db.companies import Company
from app.company.models.db.contacts import Contact
from app.company.models.shared.enums import CompanyStatus, CompanyTypes
from app.company.models.v1.contacts import ContactListModel
from app.company.utils.datetime_utils import to_timezone
from app.shared.models.db.change import Change
from app.shared.models.v1.base_out_model import BaseOutModel
from app.shared.models.v1.shared import Language
from app.shared.utils.lang_utils import select_localized_text
from app.shared.utils.request_utils import get_current_request_url_with_additions
from app.shared.utils.url_utils import assemble_profile_picture_url


def _initialize_company_model(
    cls,
    model: Company,
    lang: Language,
    tz: str | tzinfo,
    request: Request,
    router: APIRouter,
    authenticated_user: User,
    profile_picture_url: str | None,
    contacts: List[Contact] | None,
    changes: List[Change] | None,
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
        profile_picture_url=assemble_profile_picture_url(request, router, profile_picture_url, lang),
    )

    if isinstance(instance, CompanyOutModel) and contacts is not None:
        instance.contacts = [ContactListModel.from_database_model(contact, request, tz) for contact in contacts]
        try:
            if authenticated_user.is_superuser() or authenticated_user.has_role("company_admin", model.id):
                instance.changes = changes
        except AttributeError:
            pass

    return instance


class CompanyOutListModel(BaseOutModel):
    """Company model used when listing companies."""

    id: UUID
    name: str
    status: CompanyStatus
    created_date: datetime
    company_types: List[CompanyTypes]
    content_languages_iso: List[Language]
    activation_date: datetime | None
    description: str | None = Field(None)
    external_website_url: str | None
    profile_picture_url: str | None

    @classmethod
    def from_database_model(
        cls,
        model: Company,
        lang: Language,
        tz: str | tzinfo,
        request: Request,
        router: APIRouter,
        authenticated_user: User,
        profile_picture_url: str | None,
        contacts: List[Contact] | None,
        changes: List[Change] | None,
    ):
        """
        Creates model from database model with localization.
        """
        return _initialize_company_model(
            cls, model, lang, tz, request, router, authenticated_user, profile_picture_url, contacts, changes
        )


class CompanyOutModel(CompanyOutListModel):
    """Company model used when getting a single company."""

    contacts: list[ContactListModel] | None
    changes: list[Change] | None

    @classmethod
    def from_database_model(
        cls,
        model: Company,
        lang: Language,
        tz: str | tzinfo,
        request: Request,
        router: APIRouter,
        authenticated_user: User,
        profile_picture_url: str | None,
        contacts: List[Contact] | None,
        changes: List[Change] | None,
    ):
        """
        Creates model from database model with localization.
        """
        return _initialize_company_model(
            cls, model, lang, tz, request, router, authenticated_user, profile_picture_url, contacts, changes
        )


class CompanyCreateModel(BaseModel):
    """Model used when creating a new company."""

    name: dict[Language, str]
    company_types: list[CompanyTypes] = Field(..., min_items=1)
    content_languages_iso: list[Language] = Field(..., min_items=1)
    external_website_url: str | None


class CompanyUpdateModel(BaseModel):
    """Model used when updating company."""

    company_types: list[CompanyTypes] = Field(..., min_items=1)
    content_languages_iso: list[Language] = Field(..., min_items=1)
    external_website_url: str | None
