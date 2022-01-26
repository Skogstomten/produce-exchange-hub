from fastapi import APIRouter, Depends, Path, Body, Query

from app.datastores.companies_datastore import CompaniesDatastore, get_companies_datastore
from app.dependencies.app_headers import AppHeaders, get_headers
from app.models.api_list_response_model import ApiListResponseModel
from app.models.companies.company_in_model import CompanyInModel
from app.models.companies.company_out_model import CompanyOutModel
from app.models.shared.sort_order import SortOrder

router = APIRouter(
    prefix='/companies'
)


@router.get('/', response_model=ApiListResponseModel[CompanyOutModel])
def get_companies(
        headers: AppHeaders = Depends(get_headers),
        datastore: CompaniesDatastore = Depends(get_companies_datastore),
        skip: int | None = Query(0, title="Skip", description="Number of records to skip"),
        take: int | None = Query(100, title="Take", description="Max number of records to return"),
        orderby: str | None = Query(None, title="Order By", description="Sort result by field"),
        order: SortOrder | None = Query(SortOrder.asc, title="Order", description="asc or desc"),
        active_only: bool | None = Query(True, title="Active only", description="Only return active companies", alias="active-only"),
):
    companies = datastore.get_companies(headers, skip, take, orderby, order, active_only)
    return {'items': companies}


@router.get('/{company_id}', response_model=CompanyOutModel)
def get_company(
        headers: AppHeaders = Depends(get_headers),
        company_id: str = Path(...),
        datastore: CompaniesDatastore = Depends(get_companies_datastore)
):
    company = datastore.get_company(company_id, headers)
    return company


@router.post('/', response_model=CompanyOutModel)
def add_company(
        headers: AppHeaders = Depends(get_headers),
        body: CompanyInModel = Body(...),
        datastore: CompaniesDatastore = Depends(get_companies_datastore)
):
    return datastore.add_company(body, headers)


@router.post('/{company_id}/activate', response_model=CompanyOutModel)
def activate_company(
        headers: AppHeaders = Depends(get_headers),
        company_id: str = Path(...),
        datastore: CompaniesDatastore = Depends(get_companies_datastore)
):
    return datastore.activate_company(company_id, headers)
