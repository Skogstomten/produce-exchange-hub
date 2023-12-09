"""
Routing for users endpoint.
"""
from fastapi import APIRouter, Request, Body, Depends, Security, Path, status, UploadFile, File
from fastapi.responses import PlainTextResponse, FileResponse
from peewee import DoesNotExist

from app.authentication.dependencies.user import get_current_user
from app.company.models.v1.paging_information import PagingInformation, get_paging_information
from app.database.models import User
from app.logging.log import AppLoggerInjector, AppLogger
from app.shared.cryptography import password_hasher as hasher
from app.shared.dependencies.request_context import RequestContext, get_request_context
from app.shared.errors.errors import NotFoundError
from app.shared.io.file_manager import FileManager, get_file_manager
from app.shared.models.v1.paging_response_model import PagingResponseModel
from app.shared.utils.request_utils import get_url
from app.shared.utils.url_utils import assemble_profile_picture_url
from app.user.models.v1.user_api_models import UserOutModel, UserRegister

logger_injector = AppLoggerInjector("users.router")

router = APIRouter(prefix="/v1/{lang}/users", tags=["Users"])


@router.post("/register", response_model=UserOutModel)
async def register(
    request: Request,
    body: UserRegister = Body(...),
    essentials: RequestContext = Depends(get_request_context),
) -> UserOutModel:
    """
    Register new user.
    """
    data = body.model_dump()
    data.pop("password")
    data["password_hash"] = hasher.hash_password(body.password, hasher.generate_salt())
    user = User(**data)
    user.save()
    return UserOutModel.from_database_model(user, request, router, essentials.language)


@router.get("/", response_model=PagingResponseModel[UserOutModel])
async def get_users(
    authenticated_user: User = Security(get_current_user, scopes=("roles:superuser",)),
    logger: AppLogger = Depends(logger_injector),
    context: RequestContext = Depends(get_request_context),
    paging_information: PagingInformation = Depends(get_paging_information),
) -> PagingResponseModel[UserOutModel]:
    """Get list of users wrapped in a paging response object."""
    logger.debug(
        "Incoming=%s: page=%s, page_size=%s, user=%s".format(
            get_url(context.request), paging_information.page, paging_information.page_size, authenticated_user
        )
    )
    query = User.select().paginate(paging_information.page, paging_information.page_size)
    items: list[UserOutModel] = []
    for user in query:
        items.append(UserOutModel.from_database_model(user, context.request, router, context.language))
    return PagingResponseModel[UserOutModel].create(items, paging_information, context.request)


@router.get("/{user_id}", response_model=UserOutModel)
async def get_user(
    user_id: str = Path(...),
    authenticated_user: User = Security(get_current_user, scopes=("roles:superuser", "self:{user_id}")),
    context: RequestContext = Depends(get_request_context),
    logger: AppLogger = Depends(logger_injector),
) -> UserOutModel:
    """Get user by id."""
    logger.debug(f"Incoming={get_url(context.request)}: user_id={user_id}, authenticated_user={authenticated_user}")
    try:
        user = User.get_by_id(user_id)
    except DoesNotExist as ex:
        logger.warn("unable to find user %s".format(user_id), ex)
        raise NotFoundError("unable to find user %s".format(user_id))
    return UserOutModel.from_database_model(user, context.request, router, context.language)


@router.delete(
    "/{user_id}",
    response_model=None,
    responses={status.HTTP_204_NO_CONTENT: {"test": "User deleted"}},
)
async def delete_user(
    request: Request,
    user_id: str = Path(...),
    user: User = Security(get_current_user, scopes=("roles:superuser",)),
    logger: AppLogger = Depends(logger_injector),
) -> None:
    """Delete a user."""
    logger.debug(f"Incoming={get_url(request)}: user_id={user_id}, user={user}")
    try:
        user = User.get_by_id(user_id)
    except DoesNotExist as ex:
        logger.warn("Unable to find user %s".format(user_id), ex)
        raise NotFoundError(f"Unable to find user {user_id}")
    return user


@router.post("/{user_id}/profile-pictures", response_class=PlainTextResponse)
async def upload_profile_picture(
    user_id: str,
    file: UploadFile = File(...),
    authenticated_user: User = Security(
        get_current_user,
        scopes=("verified:True", "self:{user_id}"),
    ),
    context: RequestContext = Depends(get_request_context),
    file_manager: FileManager = Depends(get_file_manager),
    logger: AppLogger = Depends(logger_injector),
):
    logger.debug("upload_profile_picture(user_id=%s, authenticated_user=%s)".format(user_id, authenticated_user))
    try:
        user = User.get_by_id(user_id)
    except DoesNotExist as ex:
        logger.warn("Unable to find user %s".format(user_id), ex)
        raise NotFoundError(f"Unalbe to find user {user_id}")
    file_path = await file_manager.save_user_profile_picture(user_id, file)
    user.profile_picture_url = file_path
    user.save()
    return assemble_profile_picture_url(context.request, router, file_path, context.language)


@router.get("/profile-pictures/{image_file_name}", response_class=FileResponse)
async def get_profile_picture(
    image_file_name: str,
    file_manager: FileManager = Depends(get_file_manager),
):
    return file_manager.get_user_profile_picture_physical_path(image_file_name)
