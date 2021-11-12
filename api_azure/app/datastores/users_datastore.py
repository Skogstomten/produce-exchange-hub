from fastapi import Depends
from azure.cosmos import DatabaseProxy

from .base_datastore import BaseDatastore
from ..dependencies.auth_header import AuthHeader
from ..dependencies.cosmos_db import get_database_proxy
from ..models.users.user_out_model import UserOutModel
from ..models.users.user_in_model import UserInModel


class UsersDatastore(BaseDatastore[UserOutModel]):

    def __init__(self, db_client: DatabaseProxy):
        super(UsersDatastore, self).__init__(db_client, 'users')

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
        db: DatabaseProxy = Depends(get_database_proxy),
) -> UsersDatastore:
    return UsersDatastore(db)
