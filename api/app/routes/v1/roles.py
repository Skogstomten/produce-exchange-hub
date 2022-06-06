from fastapi import APIRouter, Depends, Body

from app.dependencies.user import get_current_user
from app.datastores.role_datastore import RoleDatastore, get_role_datastore
from app.models.v1.api_models.roles import NewRoleModel, RoleOutModel
from app.models.v1.database_models.user_database_model import UserDatabaseModel

router = APIRouter(prefix='/v1/{lang}/roles')


@router.get('/', response_model=list[RoleOutModel])
async def get_roles(
        roles: RoleDatastore = Depends(get_role_datastore)
):
    roles = roles.get_roles()
    items = []
    for role in roles:
        items.append(RoleOutModel(**role.dict()))
    return items


@router.post('/', response_model=RoleOutModel)
async def add_role(
        roles: RoleDatastore = Depends(get_role_datastore),
        body: NewRoleModel = Body(...),
        user: UserDatabaseModel = Depends(get_current_user),
):
    role = roles.add_role(body, user)
    return RoleOutModel(**role.dict())
