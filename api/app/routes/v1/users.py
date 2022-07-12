"""
Routing for users endpoint.
"""
from fastapi import APIRouter, Depends, Body, Query, Request, Security, Path, UploadFile, File
from fastapi.responses import PlainTextResponse, FileResponse
from starlette import status

from app.datastores.user_datastore import UserDatastore, get_user_datastore
from app.dependencies.essentials import Essentials, get_essentials
from app.dependencies.log import AppLogger, AppLoggerInjector
from app.dependencies.user import get_current_user
from app.models.v1.api_models.paging_response_model import PagingResponseModel
from app.models.v1.api_models.users import UserRegister, UserOutModel
from app.models.v1.database_models.user_database_model import UserDatabaseModel
from app.utils.request_utils import get_url
from app.utils.url_utils import assemble_profile_picture_url

logger_injector = AppLoggerInjector("users.router")

router = APIRouter(prefix="/v1/{lang}/users", tags=["Users"])


@router.post("/register", response_model=UserOutModel)
async def register(
    request: Request,
    user_datastore: UserDatastore = Depends(get_user_datastore),
    body: UserRegister = Body(...),
) -> UserOutModel:
    """
    Register new user.
    """
    user: UserDatabaseModel = user_datastore.add_user(body)
    return UserOutModel.from_database_model(user, request)


@router.get("/", response_model=PagingResponseModel[UserOutModel])
async def get_users(
    request: Request,
    user_datastore: UserDatastore = Depends(get_user_datastore),
    take: int = Query(20),
    skip: int = Query(0),
    user: UserDatabaseModel = Security(get_current_user, scopes=("roles:superuser",)),
    logger: AppLogger = Depends(logger_injector),
) -> PagingResponseModel[UserOutModel]:
    """Get list of users wrapped in a paging response object."""
    logger.debug(f"Incoming={get_url(request)}: take={take}, skip={skip}, user={user}")
    all_users = user_datastore.get_users(take, skip)
    items: list[UserOutModel] = []
    for usr in all_users:
        items.append(UserOutModel.from_database_model(usr, request))
    return PagingResponseModel[UserOutModel].create(items, skip, take, request)


@router.get("/{user_id}", response_model=UserOutModel)
async def get_user(
    user_id: str = Path(...),
    user_datastore: UserDatastore = Depends(get_user_datastore),
    user: UserDatabaseModel = Security(get_current_user, scopes=("roles:superuser", "self:{user_id}")),
    essentials: Essentials = Depends(get_essentials),
) -> UserOutModel:
    """Get user by id."""
    user = user_datastore.get_user_by_id(user_id, user)
    return UserOutModel.from_database_model(user, essentials.request)


@router.delete(
    "/{user_id}",
    response_model=None,
    responses={status.HTTP_204_NO_CONTENT: {"test": "User deleted"}},
)
async def delete_user(
    request: Request,
    user_datastore: UserDatastore = Depends(get_user_datastore),
    user_id: str = Path(...),
    user: UserDatabaseModel = Security(get_current_user, scopes=("roles:superuser",)),
    logger: AppLogger = Depends(logger_injector),
) -> None:
    """Delete a user."""
    logger.debug(f"Incoming={get_url(request)}: user_id={user_id}, user={user}")
    user_datastore.delete_user(user_id)


@router.post("/{user_id}/profile-pictures", response_class=PlainTextResponse)
async def upload_profile_picture(
    user_id: str,
    file: UploadFile = File(...),
    user_datastore: UserDatastore = Depends(get_user_datastore),
    authenticated_user: UserDatabaseModel = Security(
        get_current_user,
        scopes=("verified:True", "self:{user_id}", "roles:superuser"),
    ),
    essentials: Essentials = Depends(get_essentials),
):
    file_path = await user_datastore.save_profile_picture(user_id, file, authenticated_user)
    return assemble_profile_picture_url(essentials.request, router, file_path, essentials.language)


@router.get("/profile-pictures/{image_file_name}", response_class=FileResponse)
async def get_profile_picture(
    image_file_name: str,
    user_datastore: UserDatastore = Depends(get_user_datastore),
):
    return user_datastore.get_profile_picture_physical_path(image_file_name)
