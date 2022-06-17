"""Module with api models for roles."""
from pydantic import BaseModel

from ..shared import RoleType


class NewRoleModel(BaseModel):
    """Model used when adding role."""

    name: str
    type: RoleType
    description: str | None


class RoleOutModel(NewRoleModel):
    """Model used when listing roles."""

    id: str
