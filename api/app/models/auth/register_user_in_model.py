import pytz
from datetime import datetime
from typing import Dict

from pydantic import BaseModel, Field

from app.errors.invalid_timezone_error import InvalidTimezoneError


class RegisterUserInModel(BaseModel):
    username: str = Field(
        ...,
        min_length=5,
        regex="[0-9a-öA-Ö\-_\.!+#]+",
    )
    password: str = Field(
        ...,
        min_length=8,
        regex="^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$",
    )
    firstname: str = Field(
        ...,
    )
    lastname: str = Field(
        ...,
    )
    city: str = Field(
        ...,
    )
    country_iso: str = Field(
        ...,
        alias='country-iso',
    )
    timezone: str | None = Field(
        'Europe/Stockholm',
    )
    language: str | None = Field(
        'SV',
    )

    def to_database_dict(self) -> Dict[str, str | datetime]:
        if self.timezone not in pytz.all_timezones_set:
            return InvalidTimezoneError(self.timezone)

        result = {
            'username': self.username,
            'password': self.password,  # TODO: hash this
            'firstname': self.firstname,
            'lastname': self.lastname,
            'city': self.city,
            'country-iso': self.country_iso,
            'timezone': self.timezone,
            'language': self.language,
            'creation-date': datetime.now(pytz.utc)
        }
        return result
