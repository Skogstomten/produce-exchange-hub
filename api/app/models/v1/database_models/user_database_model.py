from datetime import datetime

from pydantic import BaseModel, Field

from .role_database_model import RoleDatabaseModel


class UserDatabaseModel(BaseModel):
    id: str
    email: str
    firstname: str
    lastname: str
    city: str
    country_iso: str
    timezone: str = Field('Europe/Stockholm')
    language_iso: str = Field('SV')
    verified: bool = Field(True)
    password_hash: str
    created: datetime
    last_logged_in: datetime | None
    global_roles: list[RoleDatabaseModel] = Field([])
