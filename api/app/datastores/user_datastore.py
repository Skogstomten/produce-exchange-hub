from datetime import datetime

import pytz
from fastapi import Depends

from app.cryptography import password_hasher as hasher
from app.database.document_database import DocumentDatabase, DatabaseCollection, Document
from app.dependencies.document_database import get_document_database
from app.errors.duplicate_error import DuplicateError
from app.errors.invalid_username_or_password_error import InvalidUsernameOrPasswordError
from app.errors.not_found_error import NotFoundError
from app.models.v1.api_models.users import UserAdd, UserRegister
from app.models.v1.database_models.claim_database_model import ClaimDatabaseModel
from app.models.v1.database_models.user_database_model import UserDatabaseModel, UserRoleDatabaseModel
from .role_datastore import RoleDatastore, get_role_datastore


class UserDatastore(object):
    _db: DocumentDatabase
    _roles: RoleDatastore

    def __init__(self, db: DocumentDatabase, roles: RoleDatastore):
        self._db = db
        self._roles = roles

    @property
    def _users(self) -> DatabaseCollection:
        return self._db.collection('users')

    @property
    def _claims(self) -> DatabaseCollection:
        return self._db.collection('claims')

    def get_users(self, take: int, skip: int) -> list[UserDatabaseModel]:
        docs = self._users.get_all().skip(skip).take(take).to_list()
        result = []
        for doc in docs:
            result.append(UserDatabaseModel(**doc))
        return result

    def get_users_with_role(self, role_name: str, reference: str | None = None) -> list[UserDatabaseModel]:
        if reference:
            filters = {'$and': [{'roles.role_name': role_name}, {'roles.reference': reference}]}
        else:
            filters = {'roles.role_name': role_name}
        docs = self._users.get(filters).to_list()
        return [UserDatabaseModel(**doc) for doc in docs]

    def get_company_users(self, company_id: str) -> list[UserDatabaseModel]:
        filters = {'roles.reference': company_id}
        docs = self._users.get(filters).to_list()
        return [UserDatabaseModel(**doc) for doc in docs]

    def get_user(self, email: str) -> UserDatabaseModel | None:
        doc = self._users.by_key('email', email)
        if doc is None:
            return None
        return UserDatabaseModel(**doc)

    def add_user(self, user: UserRegister) -> UserDatabaseModel:
        if self._users.exists({'email': user.email}):
            raise DuplicateError("There's already a user registered with this e-mail address")

        new_user = UserAdd(
            password_hash=hasher.hash_password(user.password, hasher.generate_salt()),
            created=datetime.now(pytz.utc),
            **user.dict()
        )
        doc = self._users.add(new_user.dict())
        return UserDatabaseModel(**doc)

    def delete_user(self, user_id: str) -> None:
        doc: Document = self._users.by_id(user_id)
        if doc is None:
            raise NotFoundError(f"No user with id '{user_id}' was found")
        doc.delete()

    def authenticate_user(self, email: str, password: str) -> UserDatabaseModel:
        doc = self._users.by_key('email', email)
        if doc is None:
            raise InvalidUsernameOrPasswordError()
        user = UserDatabaseModel(**doc)
        if not hasher.is_correct_password(password, user.password_hash):
            raise InvalidUsernameOrPasswordError()
        return user

    def add_claim(self, claim: ClaimDatabaseModel) -> ClaimDatabaseModel:
        collection = self._claims
        if collection.exists({'claim_type': claim.claim_type}):
            raise DuplicateError(f"There's already a claim with claim_type='{claim.claim_type}'")
        doc = collection.add(claim.dict())
        return ClaimDatabaseModel.from_doc(doc)

    def delete_claim(self, claim_type: str) -> ClaimDatabaseModel:
        doc = self._claims.by_key('claim_type', claim_type)
        if doc is None:
            raise NotFoundError(f"No claim with claim type '{claim_type}' was found")
        doc.delete()
        return ClaimDatabaseModel.from_doc(doc)

    def get_user_roles(
            self,
            user_id: str,
    ) -> list[UserRoleDatabaseModel]:
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
    return UserDatastore(db, roles)
