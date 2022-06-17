"""RoleDatabaseModel"""
from pydantic import BaseModel


class RoleDatabaseModel(BaseModel):
    """DB model for roles."""

    id: str
    name: str
    type: str
    description: str | None
