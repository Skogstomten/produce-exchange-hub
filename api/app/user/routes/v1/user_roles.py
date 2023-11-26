"""
Routing module for users/roles endpoint.
"""
from fastapi import APIRouter

from app.logging.log import AppLoggerInjector

logger_injector = AppLoggerInjector("user_roles_router")

router = APIRouter(prefix="/v1/users/{user_id}/roles", tags=["UserRoles"])


# @router.get("/", response_model=list[UserRoleOutModel])
# async def get_user_roles(
#     request: Request,
#     db: Engine = Depends(get_sqlalchemy_engine),
#     user_id: str = Path(...),
#     user: User = Security(get_current_user, scopes=("roles:superuser",)),
#     logger: AppLogger = Depends(logger_injector),
# ) -> list[UserRoleOutModel]:
#     """Get roles on user."""
#     logger.debug(f"Incoming={get_url(request)}: user_id={user_id}, user={user}")
#     return [UserRoleOutModel(**role.dict()) for role in user_datastore.get_user_roles(user_id)]


# @router.post("/{role_name}", response_model=UserOutModel)
# async def add_role_to_user(
#     user_datastore: UserDatastore = Depends(get_user_datastore),
#     user_id: str = Path(...),
#     role_name: str = Path(...),
#     user: User = Security(get_current_user, scopes=("roles:superuser",)),
#     essentials: Essentials = Depends(get_essentials),
# ) -> UserOutModel:
#     """Adds a role to a user."""
#     updated_user = user_datastore.add_role_to_user(user, user_id, role_name)
#     return UserOutModel.from_database_model(updated_user, essentials.request, router, essentials.language)
