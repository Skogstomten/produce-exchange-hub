"""Database models for users"""
from datetime import datetime

from pydantic import BaseModel, Field
from bson.objectid import ObjectId

from .role import RoleDatabaseModel
from ..shared import RoleType


class UserRoleDatabaseModel(BaseModel):
    """User roles model"""

    id: str
    role_id: str
    role_name: str
    role_type: RoleType
    reference: str | None

    @classmethod
    def create(cls, role: RoleDatabaseModel, reference: str | None):
        """Creates model from role database model."""
        return cls(
            id=str(ObjectId()),
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
    country_iso: str
    timezone: str = Field("Europe/Stockholm")
    language_iso: str = Field("SV")
    verified: bool = Field(True)
    password_hash: str
    created: datetime
    last_logged_in: datetime | None
    roles: list[UserRoleDatabaseModel] = Field([])
    profile_picture_url: str | None

    def is_superuser(self) -> bool:
        return any(role for role in self.roles if role.role_name == "superuser")

    def get_role(self, role_name: str) -> UserRoleDatabaseModel:
        return next((role for role in self.roles if role.role_name == role_name), None)

    def get_roles(self, role_name: str) -> list[UserRoleDatabaseModel]:
        return [role for role in self.roles if role.role_name == role_name]
