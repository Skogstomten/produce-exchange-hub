from datetime import datetime
from typing import Optional, Dict

from pydantic import BaseModel, Field

from ...datastores.base_datastore import BaseDatastore, Localization
from ...utilities.datetime_utilities import format_datetime


class UserOutModel(BaseModel):
    id: str = Field(...)
    username: str = Field(...)
    email: str = Field(...)
    firstname: str = Field(...)
    lastname: str = Field(...)
    city: str = Field(...)
    country_iso: str = Field(..., alias='countryIso')
    country: str | None = Field(None)
    created_date: datetime = Field(..., alias='createdDate')
    last_logged_in: datetime | None = Field(..., alias='lastLoggedIn')
    preferred_language_iso: str = Field(..., alias='preferredLanguageIso')
    preferred_language: Optional[str] = Field(None, alias='preferredLanguage')
    timezone: str | None = Field('Europe/Stockholm')
    profile_picture_url: str | None = Field(None, alias='profilePictureUrl')
    is_super_user: bool = Field(False, alias='isSuperUser')

    @classmethod
    def create(
            cls,
            user_id: str,
            data: Dict[str, str | datetime | bool],
            datastore: BaseDatastore,
    ):
        timezone = data.get('timezone', 'Europe/Stockholm')

        last_logged_in = data.get('last_logged_in', None)
        if last_logged_in is not None:
            last_logged_in = format_datetime(last_logged_in, timezone)

        preferred_language_iso = data.get('preferred_language_iso')
        country_iso = data.get('country_iso')
        return cls(
            id=user_id,
            username=data.get('username'),
            email=data.get('email'),
            firstname=data.get('firstname'),
            lastname=data.get('lastname'),
            city=data.get('city'),
            country_iso=country_iso,
            country=datastore.localize_from_document(
                Localization.countries_iso_name,
                country_iso,
                preferred_language_iso,
                [preferred_language_iso]
            ),
            created_date=format_datetime(data.get('created_date'), timezone),
            last_logged_in=last_logged_in,
            preferred_language_iso=preferred_language_iso,
            preferred_language=datastore.localize_from_document(
                Localization.languages_iso_name,
                preferred_language_iso,
                preferred_language_iso,
                [preferred_language_iso]
            ),
            timezone=timezone,
            profile_picture_url=data.get('profile_picture_url', None),
            is_super_user=data.get('is_super_user', False),
        )
