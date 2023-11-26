"""
Routing for users endpoint.
"""
from fastapi import APIRouter

from app.logging.log import AppLoggerInjector

logger_injector = AppLoggerInjector("users.router")

router = APIRouter(prefix="/v1/{lang}/users", tags=["Users"])


# @router.post("/register", response_model=UserOutModel)
# async def register(
#     request: Request,
#     body: UserRegister = Body(...),
#     essentials: Essentials = Depends(get_essentials),
# ) -> UserOutModel:
#     """
#     Register new user.
#     """
#     user = user_datastore.add_user(body)
#     return UserOutModel.from_database_model(user, request, router, essentials.language)


# @router.get("/", response_model=PagingResponseModel[UserOutModel])
# async def get_users(
#     user_datastore: UserDatastore = Depends(get_user_datastore),
#     take: int = Query(20),
#     skip: int = Query(0),
#     authenticated_user: User = Security(get_current_user, scopes=("roles:superuser",)),
#     logger: AppLogger = Depends(logger_injector),
#     essentials: Essentials = Depends(get_essentials),
# ) -> PagingResponseModel[UserOutModel]:
#     """Get list of users wrapped in a paging response object."""
#     logger.debug(f"Incoming={get_url(essentials.request)}: take={take}, skip={skip}, user={authenticated_user}")
#     all_users = user_datastore.get_users(take, skip)
#     items: list[UserOutModel] = []
#     for usr in all_users:
#         items.append(UserOutModel.from_database_model(usr, essentials.request, router, essentials.language))
#     return PagingResponseModel[UserOutModel].create(items, skip, take, essentials.request)


# @router.get("/{user_id}", response_model=UserOutModel)
# async def get_user(
#     user_id: str = Path(...),
#     user_datastore: UserDatastore = Depends(get_user_datastore),
#     authenticated_user: User = Security(get_current_user, scopes=("roles:superuser", "self:{user_id}")),
#     essentials: Essentials = Depends(get_essentials),
#     logger: AppLogger = Depends(logger_injector),
# ) -> UserOutModel:
#     """Get user by id."""
#     logger.debug(f"Incoming={get_url(essentials.request)}: user_id={user_id}, authenticated_user={authenticated_user}")
#     user = user_datastore.get_user_by_id(user_id)
#     return UserOutModel.from_database_model(user, essentials.request, router, essentials.language)


# @router.delete(
#     "/{user_id}",
#     response_model=None,
#     responses={status.HTTP_204_NO_CONTENT: {"test": "User deleted"}},
# )
# async def delete_user(
#     request: Request,
#     user_datastore: UserDatastore = Depends(get_user_datastore),
#     user_id: str = Path(...),
#     user: User = Security(get_current_user, scopes=("roles:superuser",)),
#     logger: AppLogger = Depends(logger_injector),
# ) -> None:
#     """Delete a user."""
#     logger.debug(f"Incoming={get_url(request)}: user_id={user_id}, user={user}")
#     user_datastore.delete_user(user_id)


# @router.post("/{user_id}/profile-pictures", response_class=PlainTextResponse)
# async def upload_profile_picture(
#     user_id: str,
#     file: UploadFile = File(...),
#     user_datastore: UserDatastore = Depends(get_user_datastore),
#     authenticated_user: User = Security(
#         get_current_user,
#         scopes=("verified:True", "self:{user_id}", "roles:superuser"),
#     ),
#     essentials: Essentials = Depends(get_essentials),
# ):
#     file_path = await user_datastore.save_profile_picture(user_id, file, authenticated_user)
#     return assemble_profile_picture_url(essentials.request, router, file_path, essentials.language)


# @router.get("/profile-pictures/{image_file_name}", response_class=FileResponse)
# async def get_profile_picture(
#     image_file_name: str,
#     user_datastore: UserDatastore = Depends(get_user_datastore),
# ):
#     return user_datastore.get_profile_picture_physical_path(image_file_name)
