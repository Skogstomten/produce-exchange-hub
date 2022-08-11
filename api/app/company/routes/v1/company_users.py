"""
Routing module for company users endpoint.
"""
from fastapi import APIRouter, Depends, Security, Path, Request, status

from app.company.datastores.company_user_datastore import get_company_user_datastore, CompanyUserDatastore
from app.user.datastores.user_datastore import UserDatastore, get_user_datastore
from app.logging.log import AppLogger, AppLoggerInjector
from app.authentication.dependencies.user import get_current_user
from app.user.models.v1.user_api_models import UserOutModel
from app.user.models.db.user import User
from app.shared.utils.request_utils import get_url

logger_injector = AppLoggerInjector("company_users_router")

router = APIRouter(prefix="/v1/{lang}/companies/{company_id}/users", tags=["CompanyUsers"])


# TODO: Consider if this should be in the user domain.
@router.get("/", response_model=list[UserOutModel])
async def get_company_users(
    request: Request,
    company_id: str = Path(...),
    user: User = Security(
        get_current_user,
        scopes=("roles:superuser", "roles:company_admin:{company_id}"),
    ),
    user_datastore: UserDatastore = Depends(get_user_datastore),
    logger: AppLogger = Depends(logger_injector),
) -> list[UserOutModel]:
    """Gets list of users with access to company."""
    logger.debug(f"Incoming={get_url(request)}: company_id={company_id}, user={user}")
    users = user_datastore.get_company_users(company_id)
    return [UserOutModel.from_database_model(u, request) for u in users]


@router.post("/{user_id}/{role_name}", response_model=list[UserOutModel], status_code=status.HTTP_201_CREATED)
async def add_user_to_company_with_role(
    request: Request,
    company_id: str = Path(...),
    user_id: str = Path(...),
    role_name: str = Path(...),
    user: User = Security(get_current_user, scopes=("roles:superuser", "roles:company_admin:{company_id}")),
    company_user_datastore: CompanyUserDatastore = Depends(get_company_user_datastore),
) -> list[UserOutModel]:
    """Adds existing user to company."""
    users = company_user_datastore.add_user_to_company(company_id, role_name, user_id, user)
    return [UserOutModel.from_database_model(u, request) for u in users]
