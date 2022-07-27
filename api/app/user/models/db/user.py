"""Database models for users"""
from datetime import datetime

from pydantic import BaseModel, Field

from app.user.models.db.role import RoleDatabaseModel
from app.shared.models.v1.shared import RoleType, CountryCode, Language


class UserRole(BaseModel):
    """User roles model"""

    id: str
    role_id: str
    role_name: str
    role_type: RoleType
    reference: str | None

    @classmethod
    def create(cls, user_role_id: str, role: RoleDatabaseModel, reference: str | None):
        """
        Creates model from role database model.
        """
        return cls(
            id=user_role_id,
            role_id=role.id,
            role_name=role.name,
            role_type=role.type,
            reference=reference,
        )


class User(BaseModel):
    """User model"""

    id: str
    email: str
    firstname: str
    lastname: str
    city: str
    country_iso: CountryCode
    timezone: str = Field("Europe/Stockholm")
    language_iso: Language = Field(Language.SV)
    verified: bool = Field(True)
    password_hash: str
    created: datetime
    last_logged_in: datetime | None
    roles: list[UserRole] = Field([])
    profile_picture_url: str | None

    def is_superuser(self) -> bool:
        return any(role for role in self.roles if role.role_name == "superuser")

    def get_role(self, role_name: str) -> UserRole:
        return next((role for role in self.roles if role.role_name == role_name), None)
