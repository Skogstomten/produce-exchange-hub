from fastapi import APIRouter, Depends, Path

from app.datastores.user_datastore import UserDatastore, get_user_datastore
from app.models.v1.api_models.roles import RoleOutModel
from app.models.v1.api_models.users import UserOutModel

router = APIRouter(prefix='/v1/users/{user_id}/roles', tags=['UserRoles'])


@router.get('/', response_model=list[RoleOutModel])
async def get_user_roles(
        user_datastore: UserDatastore = Depends(get_user_datastore),
        user_id: str = Path(...),
):
    roles = user_datastore.get_user_roles(user_id)
    items: list[RoleOutModel] = []
    for role in roles:
        items.append(RoleOutModel(**role.dict()))
    return items


@router.post('/{role_name}', response_model=UserOutModel)
async def add_role_to_user(
        user_datastore: UserDatastore = Depends(get_user_datastore),
        user_id: str = Path(...),
        role_name: str = Path(...),
):
    user = user_datastore.add_role_to_user(user_id, role_name)
    return UserOutModel.from_database_model(user)
