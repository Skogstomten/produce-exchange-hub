from datetime import datetime
from typing import Optional, Dict

from pydantic import BaseModel, Field

from ...datastores.base_datastore import BaseDatastore, Localization
from ...utilities.datetime_utilities import format_datetime


class UserOutModel(BaseModel):
    id: str = Field(...)
    first_name: str = Field(...)
    last_name: str = Field(...)
    created_date: datetime = Field(...)
    last_logged_in: Optional[datetime] = Field(...)
    preferred_language_iso: str = Field(...)
    preferred_language: Optional[str] = Field(None)
    timezone: str = Field('Europe/Stockholm')
    profile_picture_url: Optional[str] = Field(None)
    is_super_user: bool = Field(False)

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
        return cls(
            id=user_id,
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
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
