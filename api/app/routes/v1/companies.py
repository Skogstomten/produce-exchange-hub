from fastapi import APIRouter, Depends, Query, Body, Path, Request

from ...dependencies.user import get_current_user
from ...dependencies.timezone_header import get_timezone_header
from ...models.v1.api_models.companies \
    import CompanyOutListModel, CompanyOutModel, CompanyCreateModel, CompanyUpdateModel
from ...models.v1.api_models.output_list import OutputListModel
from ...models.v1.shared import Language
from ...models.v1.shared import SortOrder
from ...models.v1.users import UserInternal
from ...datastores.company_datastore import CompanyDatastore, get_company_datastore

router = APIRouter(prefix='/v1/{lang}/companies')


@router.get('/')
async def get_companies(
        request: Request,
        size: int = Query(20),
        offset: int = Query(0),
        sort_by: str | None = Query(None),
        sort_order: SortOrder = Query('asc'),
        companies: CompanyDatastore = Depends(get_company_datastore),
        lang: Language = Path(...),
        timezone: str = Depends(get_timezone_header),
):
    companies = companies.get_companies(
        offset,
        size,
        sort_by,
        sort_order
    )
    items: list[CompanyOutListModel] = []
    for company in companies:
        item = CompanyOutListModel.from_database_model(company, lang, timezone, request)
        items.append(item)
    return OutputListModel[CompanyOutListModel].create(items, len(items), offset, size, request)


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
        user: UserInternal = Depends(get_current_user),
        companies: CompanyDatastore = Depends(get_company_datastore),
        lang: Language = Path(...),
        timezone: str = Depends(get_timezone_header),
):
    company = companies.add_company(company.to_database_model())
    return CompanyOutModel.from_database_model(company, lang, timezone, request)


@router.put('/{company_id}', response_model=CompanyOutModel)
async def update_company(
        request: Request,
        company_id: str = Path(...),
        company: CompanyUpdateModel = Body(...),
        user: UserInternal = Depends(get_current_user),
        companies: CompanyDatastore = Depends(get_company_datastore),
        lang: Language = Path(...),
        timezone: str = Depends(get_timezone_header)
):
    company = companies.update_company(company.to_database_model(company_id))
    return CompanyOutModel.from_database_model(company, lang, timezone, request)
