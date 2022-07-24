"""Module with api models for roles."""
from pydantic import BaseModel

from app.shared.models.v1.shared import RoleType


class NewRoleModel(BaseModel):
    """Model used when adding role."""

    name: str
    type: RoleType
    description: str | None


class RoleOutModel(NewRoleModel):
    """Model used when listing roles."""

    id: str
