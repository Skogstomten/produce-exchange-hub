import pytz
from datetime import datetime

from fastapi import Depends

from ..dependencies.document_database import get_document_database
from ..database.document_database import DocumentDatabase
from ..cryptography import password_hasher as hasher
from ..models.v1.users import UserInternal, UserRegister, UserAdd
from ..models.v1.user_claim import UserClaim
from ..models.v1.database_models.claims import ClaimDatabaseModel
from ..errors.invalid_username_or_password_error import InvalidUsernameOrPasswordError
from ..errors.duplicate_error import DuplicateError
from ..errors.not_found_error import NotFoundError
from ..oauth2.scopes import Scopes


class UserDatastore(object):
    db: DocumentDatabase

    def __init__(self, db: DocumentDatabase):
        self.db = db

    def get_user(self, email: str) -> UserInternal | None:
        collection = self.db.collection('users')
        doc = collection.by_key('email', email)
        if doc is None:
            return None
        return UserInternal(id=doc.id, **doc.to_dict())

    def add_user(self, user: UserRegister) -> UserInternal:
        collection = self.db.collection('users')
        new_user = UserAdd(
            password_hash=hasher.hash_password(user.password, hasher.generate_salt()),
            created=datetime.now(pytz.utc),
            **user.dict()
        )
        doc = collection.add(new_user.dict())
        return UserInternal(id=doc.id, **doc.to_dict())

    def authenticate_user(self, email: str, password: str) -> UserInternal:
        collection = self.db.collection('users')
        doc = collection.by_key('email', email)
        if doc is None:
            raise InvalidUsernameOrPasswordError()
        user = UserInternal(id=doc.id, **doc.to_dict())
        if not hasher.is_correct_password(password, user.password_hash):
            raise InvalidUsernameOrPasswordError()
        return user

    def get_user_claims(self, user: UserInternal, scopes: Scopes) -> list[UserClaim]:
        pass

    def get_claims(self) -> list[ClaimDatabaseModel]:
        collection = self.db.collection('claims')
        docs = collection.get_all().to_list()
        claims = []
        for doc in docs:
            claims.append(
                ClaimDatabaseModel.from_doc(doc)
            )
        return claims

    def add_claim(self, claim: ClaimDatabaseModel) -> ClaimDatabaseModel:
        collection = self.db.collection('claims')
        if collection.exists({'claim_type': claim.claim_type}):
            raise DuplicateError(f"There's already a claim with claim_type='{claim.claim_type}'")
        doc = collection.add(claim.dict())
        return ClaimDatabaseModel.from_doc(doc)

    def delete_claim(self, claim_type: str) -> ClaimDatabaseModel:
        collection = self.db.collection('claims')
        doc = collection.by_key('claim_type', claim_type)
        if doc is None:
            raise NotFoundError()
        doc.delete()
        return ClaimDatabaseModel.from_doc(doc)


def get_user_datastore(
        db: DocumentDatabase = Depends(get_document_database)
) -> UserDatastore:
    return UserDatastore(db)
