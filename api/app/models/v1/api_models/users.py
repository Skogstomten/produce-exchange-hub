"""
Api model classes for user.
"""
from datetime import datetime

from fastapi import Request
from pydantic import BaseModel, Field

from app.utils.request_utils import get_current_request_url_with_additions
from .base_out_model import BaseOutModel
from ..database_models.user_database_model import UserDatabaseModel
from ..shared import RoleType


class UserRoleOutModel(BaseModel):
    """User roles for api output."""

    id: str
    role_id: str
    role_name: str
    role_type: RoleType
    reference: str | None


class User(BaseModel):
    """User base model."""

    email: str
    firstname: str
    lastname: str
    city: str
    country_iso: str
    timezone: str = Field("Europe/Stockholm")
    language_iso: str = Field("sv")
    verified: bool = Field(True)


class UserAdd(User):
    """Model for adding user."""

    created: datetime
    password_hash: str


class UserOutModel(User, BaseOutModel):
    """Model for returning user in api call."""

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
        """
        Creates model from database model.
        :param model: UserDatabaseModel.
        :param request: HTTP request. fastapi.Request.
        :return: New instance of UserOutModel.
        """
        return cls(
            url=get_current_request_url_with_additions(request, (str(model.id),), include_query=False),
            **model.dict(),
        )


class UserRegister(User):
    """API model when adding new user via user registration."""

    password: str
