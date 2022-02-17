from fastapi import APIRouter, Depends, Query

from ..models.output_list import OutputList
from ..models.company import CompanyPublic
from ..datastores.company_datastore import CompanyDatastore, get_company_datastore

router = APIRouter(prefix='/companies')


@router.get('/', response_model=OutputList[CompanyPublic])
async def get_companies(
        take: int | None = Query(None),
        skip: int | None = Query(None),
        sort_by: str | None = Query(None),
        sort_order: str | None = Query('asc'),
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
