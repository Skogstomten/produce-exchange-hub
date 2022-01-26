from fastapi import APIRouter, Depends, Body

from ..models.auth.register_user_in_model import RegisterUserInModel
from ..models.users.user_out_model import UserOutModel
from ..auth.auth_handler import AuthHandler, get_auth_handler

router = APIRouter(prefix='/auth')


@router.post('/register', response_model=UserOutModel)
def register_new_user(
    body: RegisterUserInModel = Body(...),
    auth_handler: AuthHandler = Depends(get_auth_handler)
):
    return auth_handler.register_new_user(body)
