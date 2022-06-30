"""
Datastore for accessing user database.
"""
from datetime import datetime

import pytz
from fastapi import Depends

from app.cryptography import password_hasher as hasher
from app.database.document_database import (
    DocumentDatabase,
    DatabaseCollection,
    Document,
)
from app.dependencies.document_database import get_document_database
from app.models.v1.api_models.users import UserAdd, UserRegister
from app.models.v1.database_models.user_database_model import (
    UserDatabaseModel,
    UserRoleDatabaseModel,
)
from .role_datastore import RoleDatastore, get_role_datastore
from ..errors import (
    DuplicateError,
    NotFoundError,
    InvalidUsernameOrPasswordError,
)


class UserDatastore:
    """
    Accesses user database.
    """

    _db: DocumentDatabase
    _roles: RoleDatastore

    def __init__(self, db: DocumentDatabase, roles: RoleDatastore):
        """
        Creates a datastore.
        :param db: DB reference.
        :param roles: Roles datastore for cross collection operations.
        """
        self._db = db
        self._roles = roles

    @property
    def _users(self) -> DatabaseCollection:
        """
        Accessor for users collection
        :return:
        """
        return self._db.collection("users")

    def get_users(self, take: int, skip: int) -> list[UserDatabaseModel]:
        """
        Get users.
        :param take: Number of users.
        :param skip: Offset.
        :return: List of UserDatabaseModel.
        """
        docs = self._users.get_all().skip(skip).take(take).to_list()
        result = []
        for doc in docs:
            result.append(UserDatabaseModel(**doc))
        return result

    def get_users_with_role(self, role_name: str, reference: str | None = None) -> list[UserDatabaseModel]:
        """
        Get users with specific role.
        :param role_name: Role name.
        :param reference: Reference, if any. For example company id for a
        company role.
        :return: List of UserDatabaseModel.
        """
        if reference:
            filters = {
                "$and": [
                    {"roles.role_name": role_name},
                    {"roles.reference": reference},
                ]
            }
        else:
            filters = {"roles.role_name": role_name}
        docs = self._users.get(filters).to_list()
        return [UserDatabaseModel(**doc) for doc in docs]

    def get_company_users(self, company_id: str) -> list[UserDatabaseModel]:
        """
        Get users with access to specified company.
        :param company_id: ID of company.
        :return: List of UserDatabaseModel.
        """
        filters = {"roles.reference": company_id}
        docs = self._users.get(filters).to_list()
        return [UserDatabaseModel(**doc) for doc in docs]

    def get_user_by_id(self, user_id: str, current_user: UserDatabaseModel) -> UserDatabaseModel:
        """
        Get user by user id.
        :raise NotFoundError: If no user with id is found
        :param user_id: ID of user.
        :param current_user: The current authenticated user.
        :return: UserDatabaseModel.
        """
        if current_user.id == user_id:
            return current_user
        doc = self._users.by_id(user_id)
        if doc is None:
            raise NotFoundError(f"No user with id '{user_id}' was found.")
        return UserDatabaseModel(**doc)

    def get_user_by_email(self, email: str) -> UserDatabaseModel | None:
        """
        Get user by email.
        :param email: EMail/UserName of user.
        :return: UserDatabaseModel or None if user was not found.
        """
        doc = self._users.by_key("email", email)
        if doc is None:
            return None
        return UserDatabaseModel(**doc)

    def add_user(self, user: UserRegister) -> UserDatabaseModel:
        """
        Add new user.
        :raise DuplcateError: If e-mail is already registered.
        :param user: New user model
        :return: UserDatabaseModel for new user.
        """
        if self._users.exists({"email": user.email}):
            raise DuplicateError("There's already a user registered with this e-mail address")

        new_user = UserAdd(
            password_hash=hasher.hash_password(user.password, hasher.generate_salt()),
            created=datetime.now(pytz.utc),
            **user.dict(),
        )
        doc = self._users.add(new_user.dict())
        return UserDatabaseModel(**doc)

    def delete_user(self, user_id: str, authenticated_user: UserDatabaseModel) -> None:
        """
        Delete user.
        :raise NotFoundError: If user with id doesn't exist.
        :param user_id: ID of user.
        :param authenticated_user: User performing operation.
        :return: None.
        """
        doc: Document = self._users.by_id(user_id)
        if doc is None:
            raise NotFoundError(f"No user with id '{user_id}' was found")
        doc.delete()

    def authenticate_user(self, email: str, password: str) -> UserDatabaseModel:
        """
        Authenticate that provided username and password matches stored.
        :raise InvalidUsernameOrPasswordError: If user can't be found with
        email or if password is not correct.
        :param email: UserName.
        :param password: Password in clear text.
        :return: UserDatabaseModel for user, if credentials are correct.
        """
        doc = self._users.by_key("email", email)
        if doc is None:
            raise InvalidUsernameOrPasswordError()
        user = UserDatabaseModel(**doc)
        if not hasher.is_correct_password(password, user.password_hash):
            raise InvalidUsernameOrPasswordError()
        return user

    def get_user_roles(
        self,
        user_id: str,
    ) -> list[UserRoleDatabaseModel]:
        """
        Get roles for user.
        :param user_id: ID of user.
        :return: List of UserRoleDatabaseModel for user.
        """
        doc = self._users.by_id(user_id)
        if doc is None:
            raise NotFoundError(f"No user with id '{user_id}' was found")
        user = UserDatabaseModel(**doc)
        return user.roles

    def add_role_to_user(
        self,
        user_id: str,
        role_name: str,
        reference: str | None = None,
    ) -> UserDatabaseModel:
        """
        Add new role to user.

        :raise NotFoundError: If user is not found.

        :param user_id: ID of user.
        :param role_name: Name of role to add.
        :param reference: Reference if role requires it.

        :return: Updated UserDatabaseModel.
        """
        user_doc = self._users.by_id(user_id)
        if user_doc is None:
            raise NotFoundError(f"No user with id '{user_id}' was found")
        role = self._roles.get_role(role_name)
        user = UserDatabaseModel(**user_doc)
        user_role = UserRoleDatabaseModel.create(role, reference)
        user.roles.append(user_role)
        user_doc = user_doc.replace(user.dict())
        return UserDatabaseModel(**user_doc)


def get_user_datastore(
    db: DocumentDatabase = Depends(get_document_database),
    roles: RoleDatastore = Depends(get_role_datastore),
) -> UserDatastore:
    """
    Dependecy injection method for user datastore.
    :param db: DB reference.
    :param roles: Roles datastore.
    :return: New UserDatastore.
    """
    return UserDatastore(db, roles)
