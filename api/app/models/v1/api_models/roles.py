from pydantic import BaseModel

from ..shared import RoleType


class NewRoleModel(BaseModel):
    name: str
    type: RoleType
    description: str | None


class RoleOutModel(NewRoleModel):
    id: str
