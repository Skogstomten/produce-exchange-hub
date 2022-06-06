from fastapi import APIRouter, Depends, Query, Body, Path, Request

from app.dependencies.user import get_current_user
from app.dependencies.timezone_header import get_timezone_header
from app.models.v1.api_models.companies \
    import CompanyOutModel, CompanyCreateModel, CompanyUpdateModel, CompanyOutListModel
from app.models.v1.api_models.output_list import OutputListModel
from app.models.v1.shared import Language
from app.models.v1.shared import SortOrder
from app.models.v1.database_models.user_database_model import UserDatabaseModel
from app.datastores.company_datastore import CompanyDatastore, get_company_datastore

router = APIRouter(prefix='/v1/{lang}/companies', tags=['Companies'])


@router.get('/', response_model=OutputListModel[CompanyOutListModel])
async def get_companies(
        request: Request,
        take: int = Query(20),
        skip: int = Query(0),
        sort_by: str | None = Query(None),
        sort_order: SortOrder = Query(SortOrder.asc),
        companies: CompanyDatastore = Depends(get_company_datastore),
        lang: Language = Path(...),
        timezone: str = Depends(get_timezone_header),
):
    companies = companies.get_companies(
        skip,
        take,
        sort_by,
        sort_order
    )
    items: list[CompanyOutListModel] = []
    for company in companies:
        item = CompanyOutListModel.from_database_model(company, lang, timezone, request)
        items.append(item)
    response = OutputListModel[CompanyOutListModel].create(items, skip, take, request)
    return response


@router.get('/{company_id}', response_model=CompanyOutModel)
async def get_company(
        request: Request,
        company_id: str = Path(...),
        companies: CompanyDatastore = Depends(get_company_datastore),
        lang: Language = Path(...),
        timezone: str = Depends(get_timezone_header)
):
    company = companies.get_company(company_id)
    return CompanyOutModel.from_database_model(company, lang, timezone, request)


@router.post('/', response_model=CompanyOutModel)
async def add_company(
        request: Request,
        company: CompanyCreateModel = Body(...),
        user: UserDatabaseModel = Depends(get_current_user),
        companies: CompanyDatastore = Depends(get_company_datastore),
        lang: Language = Path(...),
        timezone: str = Depends(get_timezone_header),
):
    company = companies.add_company(company.to_database_model(), user)
    return CompanyOutModel.from_database_model(company, lang, timezone, request)


@router.put('/{company_id}', response_model=CompanyOutModel)
async def update_company(
        request: Request,
        company_id: str = Path(...),
        company: CompanyUpdateModel = Body(...),
        user: UserDatabaseModel = Depends(get_current_user),
        companies: CompanyDatastore = Depends(get_company_datastore),
        lang: Language = Path(...),
        timezone: str = Depends(get_timezone_header)
):
    company = companies.update_company(company.to_database_model(company_id), user)
    return CompanyOutModel.from_database_model(company, lang, timezone, request)
