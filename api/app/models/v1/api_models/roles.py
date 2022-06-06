from pydantic import BaseModel

from ..database_models.role_database_model import RoleDatabaseModel


class NewRoleModel(BaseModel):
    name: str
    description: str | None


class RoleOutModel(NewRoleModel):
    id: str
