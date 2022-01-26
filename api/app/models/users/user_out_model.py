from datetime import datetime
from typing import Optional, Dict

from pydantic import BaseModel, Field

from ...datastores.base_datastore import BaseDatastore, Localization
from ...utilities.datetime_utilities import format_datetime
from ...database.document_database import Document


class UserOutModel(BaseModel):
    id: str = Field(...)
    email: str = Field(...)
    firstname: str = Field(...)
    lastname: str = Field(...)
    city: str = Field(...)
    country_iso: str | None = Field(None, alias='countryIso')
    country: str | None = Field(None)
    created_date: datetime | None = Field(None, alias='createdDate')
    last_logged_in: datetime | None = Field(None, alias='lastLoggedIn')
    preferred_language_iso: str | None = Field(None, alias='preferredLanguageIso')
    preferred_language: str | None = Field(None, alias='preferredLanguage')
    timezone: str | None = Field('Europe/Stockholm')
    profile_picture_url: str | None = Field(None, alias='profilePictureUrl')
    is_super_user: bool = Field(False, alias='isSuperUser')

    @classmethod
    def create(
            cls,
            data: Document,
            datastore: BaseDatastore,
    ):
        timezone = data.get(str, 'timezone', 'Europe/Stockholm')

        last_logged_in = data.get(datetime, 'last_logged_in', None)
        if last_logged_in is not None:
            last_logged_in = format_datetime(last_logged_in, timezone)

        preferred_language_iso = data.get(str, 'preferred_language_iso')
        country_iso = data.get(str, 'country_iso')
        return cls(
            id=data.id,
            email=data.get(str, 'email'),
            firstname=data.get(str, 'firstname'),
            lastname=data.get(str, 'lastname'),
            city=data.get(str, 'city'),
            countryIso=country_iso,
            country=datastore.localize_from_document(
                Localization.countries_iso_name,
                country_iso,
                preferred_language_iso,
                [preferred_language_iso]
            ),
            createdDate=format_datetime(data.get(datetime, 'created_date'), timezone),
            lastLoggedIn=last_logged_in,
            preferredLanguageIso=preferred_language_iso,
            preferredLanguage=datastore.localize_from_document(
                Localization.languages_iso_name,
                preferred_language_iso,
                preferred_language_iso,
                [preferred_language_iso]
            ),
            timezone=timezone,
            profilePictureUrl=data.get(str, 'profile_picture_url', None),
            isSuperUser=data.get(bool, 'is_super_user', False),
        )
