from datetime import datetime

from pydantic import BaseModel, Field

from app.models.v1.database_models.role_database_model import RoleDatabaseModel


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
    global_roles: list[RoleDatabaseModel]


class UserRegister(User):
    password: str
