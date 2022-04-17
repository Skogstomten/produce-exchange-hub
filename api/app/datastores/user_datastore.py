import pytz
from datetime import datetime

from fastapi import Depends

from ..dependencies.document_database import get_document_database
from ..database.document_database import DocumentDatabase
from ..cryptography import password_hasher as hasher
from ..models.user import UserInternal, UserRegister, UserAdd
from ..errors.invalid_username_or_password_error import InvalidUsernameOrPasswordError


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


def get_user_datastore(
        db: DocumentDatabase = Depends(get_document_database)
) -> UserDatastore:
    return UserDatastore(db)
