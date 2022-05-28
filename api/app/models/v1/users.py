from datetime import datetime

from pydantic import BaseModel, Field


class User(BaseModel):
    email: str
    firstname: str
    lastname: str
    city: str
    country_iso: str
    timezone: str = Field('Europe/Stockholm')
    language_iso: str = Field('SV')
    verified: bool = Field(True)


class UserAdd(User):
    created: datetime
    password_hash: str


class UserOut(User):
    id: str
    created: datetime
    last_logged_in: datetime | None = Field(None)


class UserInternal(UserOut, UserAdd):
    pass


class UserRegister(User):
    password: str
