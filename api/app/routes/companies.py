from fastapi import APIRouter, Depends, Query, Body, Path

from ..dependencies.user import get_current_user
from ..models.output_list import OutputList
from ..models.company import CompanyPublicOutModel, CompanyCreateModel, CompanyUpdateModel
from ..models.shared.sort_order import SortOrder
from ..models.user import UserInternal
from ..datastores.company_datastore import CompanyDatastore, get_company_datastore

router = APIRouter(prefix='/companies')


@router.get('/', response_model=OutputList[CompanyPublicOutModel])
async def get_companies(
        take: int | None = Query(None),
        skip: int | None = Query(None),
        sort_by: str | None = Query(None),
        sort_order: SortOrder | None = Query('asc'),
        companies: CompanyDatastore = Depends(get_company_datastore)
):
    companies = companies.get_companies(
        skip,
        take,
        sort_by,
        sort_order
    )
    return {
        'items': companies
    }


@router.get('/{company_id}', response_model=CompanyPublicOutModel)
async def get_company(
    company_id: str = Path(...),
    companies: CompanyDatastore = Depends(get_company_datastore),
):
    return companies.get_company(company_id)


@router.post('/', response_model=CompanyPublicOutModel)
async def add_company(
        company: CompanyCreateModel = Body(...),
        user: UserInternal = Depends(get_current_user),
        companies: CompanyDatastore = Depends(get_company_datastore),
):
    return companies.add_company(company)


@router.put('/{company_id}', response_model=CompanyPublicOutModel)
async def update_company(
        company_id: str = Path(...),
        company: CompanyUpdateModel = Body(...),
        user: UserInternal = Depends(get_current_user),
        companies: CompanyDatastore = Depends(get_company_datastore)
):
    return companies.update_company(company_id, company)
