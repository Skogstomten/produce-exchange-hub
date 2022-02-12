from datetime import datetime

from pydantic import BaseModel, Field


class User(BaseModel):
    id: str
    email: str
    firstname: str
    lastname: str
    created: datetime
    last_logged_in: datetime | None
    city: str
    country_iso: str
    timezone: str = Field('Europe/Stockholm')
    language_iso: str = Field('SV')


class UserInternal(User):
    password_hash: str
