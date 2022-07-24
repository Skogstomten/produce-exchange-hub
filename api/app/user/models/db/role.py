"""RoleDatabaseModel"""
from pydantic import BaseModel

from app.shared.models.v1.shared import RoleType


class RoleDatabaseModel(BaseModel):
    """DB model for roles."""

    id: str
    name: str
    type: RoleType
    description: str | None
