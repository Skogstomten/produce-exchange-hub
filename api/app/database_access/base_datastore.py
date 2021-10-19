from google.cloud.firestore_v1.client import Client
from .user import User
from app.errors import NotFoundError


class BaseDatastore(object):
    db: Client

    def __init__(self, db: Client):
        self.db = db

    def get_localization(self, document_key: str) -> dict[str, str]:
        document_snapshot = self.db.collection('localization').document(document_key).get()
        if document_snapshot.exists:
            return document_snapshot.to_dict()
        return {}

    def get_user(self, user_id: str) -> User:
        user_ref = self.db.collection('users').document(user_id)
        user_snapshot = user_ref.get()
        if not user_snapshot.exists:
            raise NotFoundError(user_id)

        user_data = user_snapshot.to_dict()
        return User(user_id, user_data)
