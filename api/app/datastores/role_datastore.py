from fastapi import Depends

from app.dependencies.document_database import get_document_database
from app.database.document_database import DocumentDatabase
from app.models.v1.database_models.role_database_model import RoleDatabaseModel
from app.models.v1.database_models.user_database_model import UserDatabaseModel
from app.models.v1.api_models.roles import NewRoleModel
from app.errors.duplicate_error import DuplicateError
from app.errors.unauthorized_error import UnauthorizedError


class RoleDatastore(object):
    db: DocumentDatabase

    def __init__(self, db: DocumentDatabase):
        self.db = db

    def get_roles(self) -> list[RoleDatabaseModel]:
        collection = self.db.collection('roles')
        docs = collection.get_all()
        roles = []
        for doc in docs.to_list():
            roles.append(RoleDatabaseModel(id=doc.id, **doc.to_dict()))
        return roles

    def add_role(self, model: NewRoleModel, user: UserDatabaseModel) -> RoleDatabaseModel:
        collection = self.db.collection('roles')
        if collection.exists({'name': model.name}):
            raise DuplicateError(f"Role with name '{model.name}' already exists")
        # if 'superuser' not in [role.name for role in user.global_roles]:
        #     raise UnauthorizedError()
        doc = collection.add(model.dict())
        return RoleDatabaseModel(id=doc.id, **doc.to_dict())


def get_role_datastore(
        db: DocumentDatabase = Depends(get_document_database)
) -> RoleDatastore:
    return RoleDatastore(db)
