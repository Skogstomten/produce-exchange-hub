"""
Datastore for accessing user database.
"""
from datetime import datetime

import pytz
from fastapi import Depends, UploadFile

from app.cryptography import password_hasher as hasher
from app.database.document_database import (
    DocumentDatabase,
    DatabaseCollection,
    Document,
    BaseDatastore,
)
from app.dependencies.document_database import get_document_database
from app.models.v1.api_models.users import UserAdd, UserRegister
from app.models.v1.database_models.user import (
    User,
    UserRoleDatabaseModel,
)
from .role_datastore import RoleDatastore, get_role_datastore
from ..errors import (
    DuplicateError,
    NotFoundError,
    InvalidUsernameOrPasswordError,
)
from ..io.file_manager import FileManager, get_file_manager
from ..models.v1.database_models.change import Change, ChangeType


class UserDatastore(BaseDatastore):
    """
    Accesses user database.
    """

    def __init__(self, db: DocumentDatabase, roles: RoleDatastore, file_manager: FileManager):
        """
        Creates a datastore.
        :param file_manager:
        :param db: DB reference.
        :param roles: Roles datastore for cross collection operations.
        """
        super().__init__(db)
        self._roles = roles
        self._file_manager = file_manager

    @property
    def _users(self) -> DatabaseCollection:
        """
        Accessor for users collection
        :return:
        """
        return self.db.collection("users")

    def get_users(self, take: int, skip: int) -> list[User]:
        """
        Get users.
        :param take: Number of users.
        :param skip: Offset.
        :return: List of UserDatabaseModel.
        """
        docs = self._users.get_all().skip(skip).take(take).to_list()
        result = []
        for doc in docs:
            result.append(User(**doc))
        return result

    def get_users_with_role(self, role_name: str, reference: str | None = None) -> list[User]:
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
        return [User(**doc) for doc in docs]

    def get_company_users(self, company_id: str) -> list[User]:
        """
        Get users with access to specified company.
        :param company_id: ID of company.
        :return: List of UserDatabaseModel.
        """
        filters = {"roles.reference": company_id}
        docs = self._users.get(filters).to_list()
        return [User(**doc) for doc in docs]

    def get_user_by_id(self, user_id: str, current_user: User) -> User:
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
        return User(**doc)

    def get_user_by_email(self, email: str) -> User | None:
        """
        Get user by email.
        :param email: EMail/UserName of user.
        :return: UserDatabaseModel or None if user was not found.
        """
        doc = self._users.by_key("email", email)
        if doc is None:
            return None
        return User(**doc)

    def add_user(self, user: UserRegister) -> User:
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
        return User(**doc)

    def delete_user(self, user_id: str) -> None:
        """
        Delete user.
        :raise NotFoundError: If user with id doesn't exist.
        :param user_id: ID of user.
        :return: None.
        """
        doc: Document = self._users.by_id(user_id)
        if doc is None:
            raise NotFoundError(f"No user with id '{user_id}' was found")
        doc.delete()

    def authenticate_user(self, email: str, password: str) -> User:
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
        user = User(**doc)
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
        user = User(**doc)
        return user.roles

    def add_role_to_user(
        self,
        authenticated_user: User,
        user_id: str,
        role_name: str,
        reference: str | None = None,
    ) -> User:
        """
        Add new role to user.

        :param authenticated_user: User performing the operation.
        :param user_id: ID of the user the role is getting added to.
        :param role_name: Name of role to add.
        :param reference: Reference if role requires it.

        :raise NotFoundError: If user is not found.

        :return: Updated UserDatabaseModel.
        """
        role = self._roles.get_role(role_name)
        user_role = UserRoleDatabaseModel.create(role, reference).dict()
        change = Change.create("roles", ChangeType.add, authenticated_user.email, user_role)
        update_context = self.db.update_context()
        update_context.push_to_list("roles", user_role)
        update_context.push_to_list("changes", change)
        self._users.update_document(user_id, update_context)
        return self.get_user_by_id(user_id, authenticated_user)

    async def save_profile_picture(self, user_id: str, file: UploadFile, authenticated_user: User) -> str:
        """Saves user profile picture to file storage and updates profile picture url."""
        self._ensure_user_exists(user_id)
        file_url = await self._file_manager.save_user_profile_picture(user_id, file)
        update_context = self.db.update_context()
        update_context.set_values({"profile_picture_url": file_url})
        update_context.push_to_list(
            "changes",
            Change.create(
                "profile_picture_url",
                ChangeType.update,
                authenticated_user.email,
                file_url,
            ).dict(),
        )
        self._users.update_document(user_id, update_context)
        return file_url

    def _get_user(self, user_id: str) -> User:
        user_document = self._users.by_id(user_id)
        if user_document is None:
            raise NotFoundError(f"User '{user_id}' not found")
        return User(**user_document)

    def _ensure_user_exists(self, user_id: str):
        if not self._users.exists({"id": user_id}):
            raise NotFoundError(f"User '{user_id}' not found")

    def get_profile_picture_physical_path(self, image_file_name: str) -> str:
        return self._file_manager.get_user_profile_picture_physical_path(image_file_name)


def get_user_datastore(
    db: DocumentDatabase = Depends(get_document_database),
    roles: RoleDatastore = Depends(get_role_datastore),
    file_manager: FileManager = Depends(get_file_manager),
) -> UserDatastore:
    """
    Dependecy injection method for user datastore.
    :param file_manager:
    :param db: DB reference.
    :param roles: Roles datastore.
    :return: New UserDatastore.
    """
    return UserDatastore(db, roles, file_manager)
