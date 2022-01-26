from fastapi import Depends

from .email_exists_error import EmailExistsError
from ..dependencies.document_database import get_document_database
from ..database.document_database import DocumentDatabase
from ..datastores.base_datastore import BaseDatastore
from ..models.auth.register_user_in_model import RegisterUserInModel
from ..models.users.user_out_model import UserOutModel
from ..models.auth.login_model import LoginModel
from ..cryptography.password_hasher import is_correct_password
from ..cryptography.key_generator import generate_key_from_data


class AuthHandler(BaseDatastore):
    def __init__(self, db: DocumentDatabase):
        super(AuthHandler, self).__init__(db)
    
    def register_new_user(self, model: RegisterUserInModel) -> UserOutModel:        
        if self.db.collection('users').exists({'email': model.email}):
            raise EmailExistsError(model.email)
        
        new_user = self.db.collection('users').add(model.to_database_dict())
        return UserOutModel.create(new_user, self)
    
    def login(self, model: LoginModel):
        user = self.db.collection('users').by_key('email', model.email)
        if is_correct_password(model.password, user.get(str, 'password')):
            return generate_key_from_data(
                str(user.id),
                user.get(str, 'email'),
                user.get(str, 'password')
            )


def get_auth_handler(db: DocumentDatabase = Depends(get_document_database)) -> AuthHandler:
    return AuthHandler(db)
