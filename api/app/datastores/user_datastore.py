from datetime import datetime

import pytz
from fastapi import Depends

from app.cryptography import password_hasher as hasher
from app.database.document_database import DocumentDatabase, DatabaseCollection
from app.dependencies.document_database import get_document_database
from app.errors.duplicate_error import DuplicateError
from app.errors.invalid_username_or_password_error import InvalidUsernameOrPasswordError
from app.errors.not_found_error import NotFoundError
from app.models.v1.api_models.users import UserAdd, UserRegister
from app.models.v1.database_models.claim_database_model import ClaimDatabaseModel
from app.models.v1.database_models.user_database_model import UserDatabaseModel
from app.models.v1.database_models.role_database_model import RoleDatabaseModel


class UserDatastore(object):
    db: DocumentDatabase

    def __init__(self, db: DocumentDatabase):
        self.db = db

    @property
    def _users(self) -> DatabaseCollection:
        return self.db.collection('users')

    @property
    def _roles(self) -> DatabaseCollection:
        return self.db.collection('roles')

    @property
    def _claims(self) -> DatabaseCollection:
        return self.db.collection('claims')

    def get_users(self, take: int, skip: int) -> list[UserDatabaseModel]:
        docs = self._users.get_all().skip(skip).take(take).to_list()
        result = []
        for doc in docs:
            result.append(UserDatabaseModel(**doc.to_dict()))
        return result

    def get_user(self, email: str) -> UserDatabaseModel | None:
        doc = self._users.by_key('email', email)
        if doc is None:
            return None
        return UserDatabaseModel(**doc.to_dict())

    def add_user(self, user: UserRegister) -> UserDatabaseModel:
        new_user = UserAdd(
            password_hash=hasher.hash_password(user.password, hasher.generate_salt()),
            created=datetime.now(pytz.utc),
            **user.dict()
        )
        doc = self._users.add(new_user.dict())
        return UserDatabaseModel(**doc.to_dict())

    def authenticate_user(self, email: str, password: str) -> UserDatabaseModel:
        doc = self._users.by_key('email', email)
        if doc is None:
            raise InvalidUsernameOrPasswordError()
        user = UserDatabaseModel(**doc.to_dict())
        if not hasher.is_correct_password(password, user.password_hash):
            raise InvalidUsernameOrPasswordError()
        return user

    def get_claims(self) -> list[ClaimDatabaseModel]:
        docs = self._claims.get_all().to_list()
        claims = []
        for doc in docs:
            claims.append(
                ClaimDatabaseModel.from_doc(doc)
            )
        return claims

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
    ) -> list[RoleDatabaseModel]:
        doc = self._users.by_id(user_id)
        if doc is None:
            raise NotFoundError(f"No user with id '{user_id}' was found")
        user = UserDatabaseModel(**doc.to_dict())
        return user.global_roles

    def add_role_to_user(
            self,
            user_id: str,
            role_name: str,
    ) -> UserDatabaseModel:
        user_doc = self._users.by_id(user_id)
        if user_doc is None:
            raise NotFoundError(f"No user with id '{user_id}' was found")
        role_doc = self._roles.by_key('name', role_name)
        if role_doc is None:
            raise NotFoundError(f"No role with name '{role_name}' was found")
        user = UserDatabaseModel(**user_doc)
        role = RoleDatabaseModel(**role_doc)
        user.global_roles.append(role)
        user_doc = user_doc.replace(user.dict())
        return UserDatabaseModel(**user_doc)


def get_user_datastore(
        db: DocumentDatabase = Depends(get_document_database)
) -> UserDatastore:
    return UserDatastore(db)
