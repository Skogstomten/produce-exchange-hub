from .username_exists_error import UsernameExistsError
from ..database.document_database import DocumentDatabase
from ..datastores.base_datastore import BaseDatastore
from ..models.auth.register_user_in_model import RegisterUserInModel
from ..models.users.user_out_model import UserOutModel


class AuthHandler(BaseDatastore):
    def __init__(self, db: DocumentDatabase):
        super(AuthHandler, self).__init__(db)
    
    def register_new_user(self, model: RegisterUserInModel) -> UserOutModel:
        if self.db.collection('users').exists({'username': model.username}):
            raise UsernameExistsError(model.username)
        
        new_user = self.db.collection('users').add(model.to_database_dict())
        return UserOutModel.create(new_user.id, new_user, self)
    