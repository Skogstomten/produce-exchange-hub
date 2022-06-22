"""
Routing module for company users endpoint.
"""
from fastapi import APIRouter, Depends, Security, Path, Request

from app.datastores.company_datastore import (
    CompanyDatastore,
    get_company_datastore,
)
from app.datastores.user_datastore import UserDatastore, get_user_datastore
from app.dependencies.user import get_current_user
from app.models.v1.api_models.users import UserOutModel
from app.models.v1.database_models.user_database_model import UserDatabaseModel

router = APIRouter(prefix="/v1/{lang}/companies/{company_id}/users", tags=["CompanyUsers"])


@router.get("/", response_model=list[UserOutModel])
async def get_company_users(
    request: Request,
    company_id: str = Path(...),
    user: UserDatabaseModel = Security(
        get_current_user,
        scopes=("roles:superuser", "roles:company_admin:{company_id}"),
    ),
    user_datastore: UserDatastore = Depends(get_user_datastore),
) -> list[UserOutModel]:
    """
    Gets list of users with access to company.
    :param request: http request.
    :param company_id: id of company being accessed.
    :param user: Authenticated user.
    :param user_datastore: Accesses user database.
    :return: list of users.
    """
    print(user.email)
    users = user_datastore.get_company_users(company_id)
    return [UserOutModel.from_database_model(u, request) for u in users]


@router.post("/{role_name}", response_model=list[UserOutModel])
async def add_user_to_company_with_role(
    request: Request,
    company_id: str = Path(...),
    role_name: str = Path(...),
    user: UserDatabaseModel = Security(get_current_user, scopes=("superuser", "company_admin:")),
    company_datastore: CompanyDatastore = Depends(get_company_datastore),
) -> list[UserOutModel]:
    """
    Adds existing user to company.
    :param request: http request.
    :param company_id: id of company that user is supposed to get access to.
    :param role_name: name of role to give user.
    :param user:
    :param company_datastore:
    :return:
    """
    users = company_datastore.add_user_to_company(company_id, role_name, user)
    return [UserOutModel.from_database_model(u, request) for u in users]
