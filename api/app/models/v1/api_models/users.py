from datetime import datetime

from fastapi import Request
from pydantic import BaseModel, Field

from app.utils.request_utils import get_current_request_url_with_additions
from .base_out_model import BaseOutModel
from ..database_models.user_database_model import UserDatabaseModel


class UserRoleOutModel(BaseModel):
    id: str
    role_id: str
    role_name: str
    role_type: str
    reference: str | None


class User(BaseModel):
    email: str
    firstname: str
    lastname: str
    city: str
    country_iso: str
    timezone: str = Field("Europe/Stockholm")
    language_iso: str = Field("sv")
    verified: bool = Field(True)


class UserAdd(User):
    created: datetime
    password_hash: str


class UserOutModel(User, BaseOutModel):
    id: str
    created: datetime
    last_logged_in: datetime | None = Field(None)
    roles: list[UserRoleOutModel]

    @classmethod
    def from_database_model(
        cls,
        model: UserDatabaseModel,
        request: Request,
    ) -> "UserOutModel":
        return cls(
            url=get_current_request_url_with_additions(
                request, (str(model.id),), include_query=False
            ),
            **model.dict(),
        )


class UserRegister(User):
    password: str
