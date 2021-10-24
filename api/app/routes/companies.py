from fastapi import APIRouter, Header, Depends, Path

from app.datastores.companies_datastore import CompaniesDatastore, get_companies_datastore
from app.models.api_list_response_model import ApiListResponseModel
from app.models.companies.company_api_list_model import CompanyApiListModel
from app.models.companies.company_out_model import CompanyOutModel

router = APIRouter(
    prefix='/companies'
)


@router.get('/', response_model=ApiListResponseModel[CompanyApiListModel])
def get_companies(
        language: str = Header('SV', min_length=2, max_length=2),
        datastore: CompaniesDatastore = Depends(get_companies_datastore)
):
    companies = datastore.get_companies(language)
    return {'items': companies}


@router.get('/{company_id}', response_model=CompanyOutModel)
def get_company(
        language: str = Header('SV', min_length=2, max_length=2),
        company_id: str = Path(...),
        datastore: CompaniesDatastore = Depends(get_companies_datastore)
):
    company = datastore.get_company(company_id, language)
    return company
