from fastapi import APIRouter, Depends, Security, Path, Request

from app.dependencies.user import get_current_user
from app.models.v1.api_models.users import UserOutModel
from app.models.v1.database_models.user_database_model import UserDatabaseModel
from app.datastores.company_datastore import CompanyDatastore, get_company_datastore
from app.datastores.user_datastore import UserDatastore, get_user_datastore

router = APIRouter(prefix='/v1/{lang}/companies/{company_id}/users', tags=['CompanyUsers'])


@router.get('/', response_model=list[UserOutModel])
async def get_company_users(
        request: Request,
        company_id: str = Path(...),
        user: UserDatabaseModel = Security(
            get_current_user,
            scopes=('roles:superuser', 'roles:company_admin:{company_id}')
        ),
        user_datastore: UserDatastore = Depends(get_user_datastore),
):
    users = user_datastore.get_company_users(company_id)
    return [UserOutModel.from_database_model(u, request) for u in users]


@router.post('/{role_name}', response_model=list[UserOutModel])
async def add_user_to_company_with_role(
        request: Request,
        company_id: str = Path(...),
        role_name: str = Path(...),
        user: UserDatabaseModel = Security(get_current_user, scopes=('superuser', 'company_admin:')),
        company_datastore: CompanyDatastore = Depends(get_company_datastore),
):
    users = company_datastore.add_user_to_company(company_id, role_name, user)
    return [UserOutModel.from_database_model(u, request) for u in users]
