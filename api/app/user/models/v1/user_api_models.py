"""
Api model classes for user.
"""
from datetime import datetime

from fastapi import Request, APIRouter
from pydantic import BaseModel, Field

from app.shared.utils.request_utils import get_current_request_url_with_additions
from app.shared.models.v1.base_out_model import BaseOutModel
from app.shared.utils.url_utils import assemble_profile_picture_url
from app.user.models.db.user import User as UserDatabaseModel
from app.shared.models.v1.shared import RoleType, CountryCode, Language


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
    country_iso: CountryCode
    timezone: str = Field("Europe/Stockholm")
    language_iso: Language = Field(Language.SV)
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
    roles: list[UserRoleOutModel] = Field([])
    profile_picture_url: str | None

    @classmethod
    def from_database_model(
        cls,
        model: UserDatabaseModel,
        request: Request,
        router: APIRouter,
        language: Language,
    ) -> "UserOutModel":
        """
        Creates model from database model.
        :param language:
        :param router:
        :param model: UserDatabaseModel.
        :param request: HTTP request. fastapi.Request.
        :return: New instance of UserOutModel.
        """
        instance = cls(
            url=get_current_request_url_with_additions(request, (str(model.id),), include_query=False),
            **model.model_dump(),
        )

        if instance.profile_picture_url:
            instance.profile_picture_url = assemble_profile_picture_url(
                request, router, instance.profile_picture_url, language
            )
        else:
            instance.profile_picture_url = None
        return instance


class UserRegister(User):
    """API model when adding new user via user registration."""

    password: str
