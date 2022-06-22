"""
Route module for roles endpoint.
"""
from fastapi import APIRouter, Depends, Body, Security

from app.dependencies.user import get_current_user
from app.datastores.role_datastore import RoleDatastore, get_role_datastore
from app.models.v1.api_models.roles import NewRoleModel, RoleOutModel
from app.models.v1.database_models.user_database_model import UserDatabaseModel

router = APIRouter(prefix="/v1/{lang}/roles", tags=["Roles"])


@router.get("/", response_model=list[RoleOutModel])
async def get_roles(
    role_datastore: RoleDatastore = Depends(get_role_datastore),
    user: UserDatabaseModel = Security(get_current_user, scopes=("roles:superuser",)),
) -> list[RoleOutModel]:
    """
    Gets a list of all roles.
    :param role_datastore: Accesses role database collection.
    :param user: Current authenticated user.
    :return: list of role model objects.
    """
    print(f"get_roles called by {user.email}")
    role_datastore = role_datastore.get_roles()
    items = []
    for role in role_datastore:
        items.append(RoleOutModel(**role.dict()))
    return items


@router.post("/", response_model=RoleOutModel)
async def add_role(
    roles_datastore: RoleDatastore = Depends(get_role_datastore),
    body: NewRoleModel = Body(...),
    user: UserDatabaseModel = Security(get_current_user, scopes=("roles:superuser",)),
) -> RoleOutModel:
    """
    Adds new role.
    Only accessible to superusers.
    :param roles_datastore: Accesses roles database collection.
    :param body: http request body as model object.
    :param user: current authenticated user.
    :return:
    """
    print(f"Role {body.name} added by user {user.email}")
    role = roles_datastore.add_role(body)
    return RoleOutModel(**role.dict())
