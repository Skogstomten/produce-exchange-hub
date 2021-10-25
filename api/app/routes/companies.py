from fastapi import APIRouter, Depends, Path

from app.datastores.companies_datastore import CompaniesDatastore, get_companies_datastore
from app.dependencies.app_headers import AppHeaders, get_headers
from app.models.api_list_response_model import ApiListResponseModel
from app.models.companies.company_api_list_model import CompanyApiListModel
from app.models.companies.company_out_model import CompanyOutModel

router = APIRouter(
    prefix='/companies'
)


@router.get('/', response_model=ApiListResponseModel[CompanyApiListModel])
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
