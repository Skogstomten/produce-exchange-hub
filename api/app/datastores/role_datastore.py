"""
Module for RolesDatastore.
"""
from fastapi import Depends

from app.database.document_database import DocumentDatabase, DatabaseCollection
from app.dependencies.document_database import get_document_database
from app.errors import NotFoundError, DuplicateError
from app.models.v1.api_models.roles import NewRoleModel
from app.models.v1.database_models.role_database_model import RoleDatabaseModel


class RoleDatastore:
    """
    Handles data access related to roles.
    """

    db: DocumentDatabase

    def __init__(self, db: DocumentDatabase):
        """
        Creates a RolesDatastore.
        :param db: DB reference.
        """
        self.db = db

    @property
    def _roles(self) -> DatabaseCollection:
        """
        Accessor for roles collection.
        :return: DatabaseCollection
        """
        return self.db.collection("roles")

    def get_roles(self) -> list[RoleDatabaseModel]:
        """
        Get all roles.
        :return: List of RoleDatabaseModel.
        """
        docs = self._roles.get_all()
        roles = []
        for doc in docs.to_list():
            roles.append(RoleDatabaseModel(id=doc.id, **doc.to_dict()))
        return roles

    def get_role(self, role_name: str) -> RoleDatabaseModel:
        """
        Get role.
        :raise NotFoundError: If role with name is not found.
        :param role_name: Name of role to get.
        :return: RoleDatabaseModel.
        """
        doc = self._roles.by_key("name", role_name)
        if doc is None:
            raise NotFoundError(f"Role with name '{role_name}' was not found")
        return RoleDatabaseModel(**doc)

    def add_role(self, model: NewRoleModel) -> RoleDatabaseModel:
        """
        Add new role.
        :raise DuplicateError: If role with name already exsists.
        :param model: New role data.
        :return: RoleDatabaseModel
        """
        collection = self.db.collection("roles")
        if collection.exists({"name": model.name}):
            raise DuplicateError(f"Role with name '{model.name}' already exists")
        doc = collection.add(model.dict())
        return RoleDatabaseModel(id=doc.id, **doc.to_dict())


def get_role_datastore(
    db: DocumentDatabase = Depends(get_document_database),
) -> RoleDatastore:
    """
    DI injection funciton.
    :param db: DB reference.
    :return: RoleDatastore
    """
    return RoleDatastore(db)
