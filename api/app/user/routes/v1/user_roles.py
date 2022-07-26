"""
Routing module for users/roles endpoint.
"""
from fastapi import APIRouter, Depends, Path, Request, Security

from app.logging.log import AppLogger, AppLoggerInjector
from app.authentication.dependencies.user import get_current_user
from app.user.datastores.user_datastore import UserDatastore, get_user_datastore
from app.user.models.v1.users import UserOutModel, UserRoleOutModel
from app.user.models.db.user import User
from app.shared.utils.request_utils import get_url

logger_injector = AppLoggerInjector("user_roles_router")

router = APIRouter(prefix="/v1/users/{user_id}/roles", tags=["UserRoles"])


@router.get("/", response_model=list[UserRoleOutModel])
async def get_user_roles(
    request: Request,
    user_datastore: UserDatastore = Depends(get_user_datastore),
    user_id: str = Path(...),
    user: User = Security(get_current_user, scopes=("roles:superuser",)),
    logger: AppLogger = Depends(logger_injector),
) -> list[UserRoleOutModel]:
    """Get roles on user."""
    logger.debug(f"Incoming={get_url(request)}: user_id={user_id}, user={user}")
    return [UserRoleOutModel(**role.dict()) for role in user_datastore.get_user_roles(user_id)]


@router.post("/{role_name}", response_model=UserOutModel)
async def add_role_to_user(
    request: Request,
    user_datastore: UserDatastore = Depends(get_user_datastore),
    user_id: str = Path(...),
    role_name: str = Path(...),
    user: User = Security(get_current_user, scopes=("roles:superuser",)),
) -> UserOutModel:
    """Adds a role to a user."""
    updated_user = user_datastore.add_role_to_user(user, user_id, role_name)
    return UserOutModel.from_database_model(updated_user, request)
