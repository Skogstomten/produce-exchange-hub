from fastapi import APIRouter, Depends, Path, Body

from app.datastores.companies_datastore import CompaniesDatastore, get_companies_datastore
from app.dependencies.app_headers import AppHeaders, get_headers
from app.models.api_list_response_model import ApiListResponseModel
from app.models.companies.company_in_model import CompanyInModel
from app.models.companies.company_out_model import CompanyOutModel

router = APIRouter(
    prefix='/companies'
)


@router.get('/', response_model=ApiListResponseModel[CompanyOutModel])
def get_companies(
        headers: AppHeaders = Depends(get_headers),
        datastore: CompaniesDatastore = Depends(get_companies_datastore)
):
    companies = datastore.get_companies(headers)
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
