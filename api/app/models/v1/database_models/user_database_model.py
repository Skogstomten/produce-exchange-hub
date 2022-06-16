from datetime import datetime

from pydantic import BaseModel, Field
from bson.objectid import ObjectId

from .role_database_model import RoleDatabaseModel


class UserRoleDatabaseModel(BaseModel):
    id: str
    role_id: str
    role_name: str
    role_type: str
    reference: str | None

    @classmethod
    def create(cls, role: RoleDatabaseModel, reference: str | None):
        return cls(
            id=str(ObjectId()),
            role_id=role.id,
            role_name=role.name,
            role_type=role.type,
            reference=reference,
        )


class UserDatabaseModel(BaseModel):
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
