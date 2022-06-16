from fastapi import Depends

from app.database.document_database import DocumentDatabase
from app.dependencies.document_database import get_document_database
from app.errors.duplicate_error import DuplicateError
from app.errors.not_found_error import NotFoundError
from app.models.v1.api_models.roles import NewRoleModel
from app.models.v1.database_models.role_database_model import RoleDatabaseModel


class RoleDatastore(object):
    db: DocumentDatabase

    def __init__(self, db: DocumentDatabase):
        self.db = db

    @property
    def _roles(self):
        return self.db.collection("roles")

    def get_roles(self) -> list[RoleDatabaseModel]:
        docs = self._roles.get_all()
        roles = []
        for doc in docs.to_list():
            roles.append(RoleDatabaseModel(id=doc.id, **doc.to_dict()))
        return roles

    def get_role(self, role_name: str) -> RoleDatabaseModel:
        doc = self._roles.by_key("name", role_name)
        if doc is None:
            raise NotFoundError(f"Role with name '{role_name}' was not found")
        return RoleDatabaseModel(**doc)

    def add_role(self, model: NewRoleModel) -> RoleDatabaseModel:
        collection = self.db.collection("roles")
        if collection.exists({"name": model.name}):
            raise DuplicateError(f"Role with name '{model.name}' already exists")
        doc = collection.add(model.dict())
        return RoleDatabaseModel(id=doc.id, **doc.to_dict())


def get_role_datastore(
    db: DocumentDatabase = Depends(get_document_database),
) -> RoleDatastore:
    return RoleDatastore(db)
