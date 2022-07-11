"""
Route module for roles endpoint.
"""
from fastapi import APIRouter, Depends, Body, Security
from starlette.requests import Request

from app.dependencies.log import AppLogger, AppLoggerInjector
from app.dependencies.user import get_current_user
from app.datastores.role_datastore import RoleDatastore, get_role_datastore
from app.models.v1.api_models.roles import NewRoleModel, RoleOutModel
from app.models.v1.database_models.user_database_model import UserDatabaseModel
from app.utils.request_utils import get_url

logger_injector = AppLoggerInjector("roles_router")

router = APIRouter(prefix="/v1/{lang}/roles", tags=["Roles"])


@router.get("/", response_model=list[RoleOutModel])
async def get_roles(
    request: Request,
    role_datastore: RoleDatastore = Depends(get_role_datastore),
    user: UserDatabaseModel = Security(get_current_user, scopes=("roles:superuser",)),
    logger: AppLogger = Depends(logger_injector),
) -> list[RoleOutModel]:
    """Gets a list of all roles."""
    logger.debug(f"Incoming={get_url(request)}: user={user}")
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
    """
    role = roles_datastore.add_role(body, user)
    return RoleOutModel(**role.dict())
