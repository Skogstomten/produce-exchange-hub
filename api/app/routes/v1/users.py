from fastapi import APIRouter, Depends, Body

from app.datastores.user_datastore import UserDatastore, get_user_datastore
from app.models.v1.api_models.users import UserRegister, UserOut

router = APIRouter(prefix='/v1/users')


@router.post('/register', response_model=UserOut)
async def register(
        users: UserDatastore = Depends(get_user_datastore),
        body: UserRegister = Body(...)
):
    user = users.add_user(body)
    return UserOut(**user.dict())
