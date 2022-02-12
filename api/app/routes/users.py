from fastapi import APIRouter, Depends, Body

from ..datastores.user_datastore import UserDatastore, get_user_datastore
from ..models.user import UserRegister, UserOut

router = APIRouter(prefix='/users')


@router.post('/register', response_model=UserOut)
async def register(
        users: UserDatastore = Depends(get_user_datastore),
        body: UserRegister = Body(...)
):
    user = users.add_user(body)
    return UserOut(**user.dict())
