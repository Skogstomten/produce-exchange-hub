"""
Routing for users endpoint.
"""
from fastapi import APIRouter, Depends, Body, Query, Request, Security, Path

from app.dependencies.user import get_current_user
from app.datastores.user_datastore import UserDatastore, get_user_datastore
from app.models.v1.api_models.paging_response_model import PagingResponseModel
from app.models.v1.api_models.users import UserRegister, UserOutModel
from app.models.v1.database_models.user_database_model import UserDatabaseModel

router = APIRouter(prefix="/v1/users", tags=["Users"])


@router.post("/register", response_model=UserOutModel)
async def register(
    request: Request,
    user_datastore: UserDatastore = Depends(get_user_datastore),
    body: UserRegister = Body(...),
) -> UserOutModel:
    """
    Register new user.
    :param request: http request.
    :param user_datastore: datastore to access user database.
    :param body: http request body object.
    :return: UserOutModel
    """
    user: UserDatabaseModel = user_datastore.add_user(body)
    return UserOutModel.from_database_model(user, request)


@router.get("/", response_model=PagingResponseModel[UserOutModel])
async def get_users(
    request: Request,
    user_datastore: UserDatastore = Depends(get_user_datastore),
    take: int = Query(20),
    skip: int = Query(0),
    user: UserDatabaseModel = Security(
        get_current_user, scopes=("roles:superuser",)
    ),
) -> PagingResponseModel[UserOutModel]:
    """
    Get list of users wrapped in a paging response object.
    :param request: http request object.
    :param user_datastore: for accessing user database.
    :param take: Number of users to return in each response.
    :param skip: Number users to skip. For paging.
    :param user: Current authenticated user, for security checking.
    :return: PagingResponseModel[UserOutModel].
    """
    print(f"User {user.email} is accessing roles.")
    all_users = user_datastore.get_users(take, skip)
    items: list[UserOutModel] = []
    for usr in all_users:
        items.append(UserOutModel.from_database_model(usr, request))
    return PagingResponseModel[UserOutModel].create(items, skip, take, request)


@router.delete(
    "/{user_id}",
    response_model=None,
    responses={200: {"test": "User deleted"}},
)
async def delete_user(
    user_datastore: UserDatastore = Depends(get_user_datastore),
    user_id: str = Path(...),
    user: UserDatabaseModel = Security(
        get_current_user, scopes=("roles:superuser",)
    ),
) -> None:
    """
    Delete a user.

    :param user_datastore: Accesses user database.
    :param user_id: id of user to be deleted.
    :param user: Current authenticated user for authentication.
    :return: None.
    """
    print(f"User {user.email} is deleting user {user_id}")
    user_datastore.delete_user(user_id)
