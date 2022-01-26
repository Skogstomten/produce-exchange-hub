import pytz
from datetime import datetime
from typing import Dict

from pydantic import BaseModel, Field

from ...errors.invalid_timezone_error import InvalidTimezoneError
from ...cryptography import password_hasher as hasher


class RegisterUserInModel(BaseModel):
    password: str = Field(
        ...,
        min_length=8,
        regex="^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$",
    )
    email: str = Field(
        ...,
        regex="(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])",
    )
    firstname: str = Field(...)
    lastname: str = Field(...)
    city: str = Field(...)
    country_iso: str = Field(...)
    timezone: str | None = Field('Europe/Stockholm')
    preferred_language_iso: str | None = Field('SV')

    def to_database_dict(self) -> Dict[str, str | datetime | bool | None]:
        if self.timezone not in pytz.all_timezones_set:
            raise InvalidTimezoneError(self.timezone)
        
        hashed_password = hasher.hash_password(
            self.password,
            hasher.generate_salt()
        )

        result = {
            'email': self.email,
            'password': hashed_password,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'city': self.city,
            'country_iso': self.country_iso,
            'created_date': datetime.now(pytz.utc),
            'last_logged_in': None,
            'preferred_language_iso': self.preferred_language_iso,
            'timezone': self.timezone,
            'profile_picture_url': None,
            'is_super_user': False
        }
        return result
