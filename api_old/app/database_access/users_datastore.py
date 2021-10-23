from .firestore import get_db_client as get_db
from .base_datastore import BaseDatastore
from .user import User


class UsersDatastore(BaseDatastore):
    def __init__(self):
        super(UsersDatastore, self).__init__(get_db())

    def list_users(self) -> list[User]:
        user_snapshots = self.db.collection('users').get()
        for user_snapshot in user_snapshots:
            yield User(user_snapshot.id, user_snapshot.to_dict())
