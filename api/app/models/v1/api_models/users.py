from datetime import datetime

from pydantic import BaseModel, Field

from .base_out_model import BaseOutModel
from ..database_models.role_database_model import RoleDatabaseModel
from ..database_models.user_database_model import UserDatabaseModel


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


class UserOutModel(User, BaseOutModel):
    id: str
    created: datetime
    last_logged_in: datetime | None = Field(None)
    global_roles: list[RoleDatabaseModel]

    @classmethod
    def from_database_model(cls, model: UserDatabaseModel):
        return cls(
            **model.dict(),
        )


class UserRegister(User):
    password: str
