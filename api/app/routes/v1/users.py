from fastapi import APIRouter, Depends, Body, Query, Request, Security

from app.dependencies.user import get_current_user
from app.datastores.user_datastore import UserDatastore, get_user_datastore
from app.models.v1.api_models.output_list import OutputListModel
from app.models.v1.api_models.users import UserRegister, UserOutModel
from app.models.v1.database_models.user_database_model import UserDatabaseModel

router = APIRouter(prefix='/v1/users', tags=['Users'])


@router.post('/register', response_model=UserOutModel)
async def register(
        users: UserDatastore = Depends(get_user_datastore),
        body: UserRegister = Body(...)
):
    user = users.add_user(body)
    return UserOutModel(**user.dict())


@router.get('/', response_model=OutputListModel[UserOutModel])
async def get_users(
        request: Request,
        user_datastore: UserDatastore = Depends(get_user_datastore),
        take: int = Query(20),
        skip: int = Query(0),
        user: UserDatabaseModel = Security(get_current_user, scopes=('roles:superuser',)),
):
    all_users = user_datastore.get_users(take, skip)
    items: list[UserOutModel] = []
    for user in all_users:
        items.append(UserOutModel.from_database_model(user))
    return OutputListModel[UserOutModel].create(items, skip, take, request)
