from google.cloud.firestore_v1.client import Client
from fastapi import Depends

from .base_datastore import BaseDatastore
from ..dependencies.firestore import get_db_client
from ..models.users.user_out_model import UserOutModel


class UsersDatastore(BaseDatastore[UserOutModel]):
    def __init__(self, db: Client):
        super(UsersDatastore, self).__init__(db, 'users')

    def get_user(
            self,
            user_id: str
    ) -> UserOutModel:
        return self.get(
            user_id,
            lambda doc_id, data: UserOutModel.create(doc_id, data, self)
        )


def get_users_datastore(
        db: Client = Depends(get_db_client)
) -> UsersDatastore:
    return UsersDatastore(db)
