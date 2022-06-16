"""
Routing module for users/roles endpoint.
"""
from fastapi import APIRouter, Depends, Path, Request, Security

from app.dependencies.user import get_current_user
from app.datastores.user_datastore import UserDatastore, get_user_datastore
from app.models.v1.api_models.users import UserOutModel, UserRoleOutModel
from app.models.v1.database_models.user_database_model import UserDatabaseModel

router = APIRouter(prefix="/v1/users/{user_id}/roles", tags=["UserRoles"])


@router.get("/", response_model=list[UserRoleOutModel])
async def get_user_roles(
    user_datastore: UserDatastore = Depends(get_user_datastore),
    user_id: str = Path(...),
    user: UserDatabaseModel = Depends(get_current_user),
) -> list[UserRoleOutModel]:
    """
    Get roles on user.
    :param user_datastore: For accessing user database.
    :param user_id: Id of user to get roles for.
    :param user: Current authenticated user for authorization.
    :return: list of UserRoleOutModel.
    """
    print(f"User {user.email} is accessing user roles for user {user_id}")
    roles = user_datastore.get_user_roles(user_id)
    items: list[UserRoleOutModel] = []
    for role in roles:
        items.append(UserRoleOutModel(**role.dict()))
    return items


@router.post("/{role_name}", response_model=UserOutModel)
async def add_role_to_user(
    request: Request,
    user_datastore: UserDatastore = Depends(get_user_datastore),
    user_id: str = Path(...),
    role_name: str = Path(...),
    user: UserDatabaseModel = Security(..., scopes=("roles:superuser",)),
) -> UserOutModel:
    """
    Adds a role to a user.
    :param request: http request.
    :param user_datastore: user database access.
    :param user_id: user id of user to add role to.
    :param role_name: name of role to add.
    :param user: Current authenticated user for authorization.
    :return: Updated user.
    """
    print(f"User {user.email} adding role {role_name} to user {user_id}")
    user = user_datastore.add_role_to_user(user_id, role_name)
    return UserOutModel.from_database_model(user, request)
