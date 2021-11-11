from google.cloud.firestore_v1.client import Client
from firebase_admin.auth import Client as AuthClient
from fastapi import Depends

from .base_datastore import BaseDatastore
from ..dependencies.firestore import get_db_client
from ..dependencies.firebase_auth import get_auth_client
from ..dependencies.auth_header import AuthHeader
from ..models.users.user_out_model import UserOutModel
from ..models.users.user_in_model import UserInModel


class UsersDatastore(BaseDatastore[UserOutModel]):
    auth_client: AuthClient

    def __init__(self, db_client: Client, auth_client: AuthClient):
        super(UsersDatastore, self).__init__(db_client, 'users')
        self.auth_client = auth_client

    def get_user(
            self,
            user_id: str
    ) -> UserOutModel:
        return self.get(
            user_id,
            lambda doc_id, data: UserOutModel.create(doc_id, data, self)
        )

    def add_user(
            self,
            in_model: UserInModel,
            auth_header: AuthHeader
    ) -> UserOutModel:
        pass


def get_users_datastore(
        db: Client = Depends(get_db_client),
        auth: AuthClient = Depends(get_auth_client),
) -> UsersDatastore:
    return UsersDatastore(db, auth)
