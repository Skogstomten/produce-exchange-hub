"""
Routing module for companies endpoint.
"""
from fastapi import APIRouter, Depends, Query, Body, Path, Request, Security

from app.datastores.company_datastore import (
    CompanyDatastore,
    get_company_datastore,
)
from app.dependencies.essentials import Essentials, get_essentials
from app.dependencies.paging_information import (
    PagingInformation,
    get_paging_information,
)
from app.dependencies.timezone_header import get_timezone_header
from app.dependencies.user import get_current_user
from app.models.v1.api_models.companies import (
    CompanyOutModel,
    CompanyCreateModel,
    CompanyUpdateModel,
    CompanyOutListModel,
)
from app.models.v1.api_models.paging_response_model import PagingResponseModel
from app.models.v1.database_models.user_database_model import UserDatabaseModel
from app.models.v1.shared import Language
from app.models.v1.shared import SortOrder

router = APIRouter(prefix="/companies", tags=["Companies"])


@router.get("/", response_model=PagingResponseModel[CompanyOutListModel])
async def get_companies(
    sort_by: str | None = Query(None),
    sort_order: SortOrder = Query(SortOrder.asc),
    company_datastore: CompanyDatastore = Depends(get_company_datastore),
    essentials: Essentials = Depends(get_essentials),
    paging_information: PagingInformation = Depends(get_paging_information),
) -> PagingResponseModel[CompanyOutListModel]:
    """
    Get list of companies wrapped in a paging response.
    :param paging_information: Data needed for paging.
    :param essentials: Essential dependencies.
    :param sort_by: Sort by value name.
    :param sort_order: Value=asc or desc.
    :param company_datastore:
    :return: PagingResponseModel of CompanyOutListModel.
    """
    company_datastore = company_datastore.get_companies(
        paging_information.skip, paging_information.take, sort_by, sort_order
    )
    items: list[CompanyOutListModel] = []
    for company in company_datastore:
        item = CompanyOutListModel.from_database_model(
            company,
            essentials.language,
            essentials.timezone,
            essentials.request,
        )
        items.append(item)
    response = PagingResponseModel[CompanyOutListModel].create(
        items,
        paging_information.skip,
        paging_information.take,
        essentials.request,
    )
    return response


@router.get("/{company_id}", response_model=CompanyOutModel)
async def get_company(
    request: Request,
    company_id: str = Path(...),
    company_datastore: CompanyDatastore = Depends(get_company_datastore),
    lang: Language = Path(...),
    timezone: str = Depends(get_timezone_header),
) -> CompanyOutModel:
    """
    Get a company by id.
    :param request: HTTP request.
    :param company_id: ID of company.
    :param company_datastore: Company database access.
    :param lang: User language.
    :param timezone: User timezone.
    :return: CompanyOutModel.
    """
    company = company_datastore.get_company(company_id)
    return CompanyOutModel.from_database_model(
        company, lang, timezone, request
    )


@router.post("/", response_model=CompanyOutModel)
async def add_company(
    company: CompanyCreateModel = Body(...),
    user: UserDatabaseModel = Security(
        get_current_user, scopes=("verified:True",)
    ),
    company_datastore: CompanyDatastore = Depends(get_company_datastore),
    essentials: Essentials = Depends(get_essentials),
) -> CompanyOutModel:
    """
    Add a new company.
    :param essentials:
    :param company: HTTP request body serialized to model object.
    :param user: Current authenticated user.
    :param company_datastore: Company database access class.
    :return: CompanyOutModel.
    """
    company = company_datastore.add_company(company, user)
    return CompanyOutModel.from_database_model(
        company, essentials.language, essentials.timezone, essentials.request
    )


@router.put("/{company_id}", response_model=CompanyOutModel)
async def update_company(
    company_id: str = Path(...),
    company: CompanyUpdateModel = Body(...),
    user: UserDatabaseModel = Security(
        get_current_user,
        scopes=(
            "roles:company_admin:{company_id}",
            "roles:superuser",
        ),
    ),
    company_datastore: CompanyDatastore = Depends(get_company_datastore),
    essentials: Essentials = Depends(get_essentials),
) -> CompanyOutModel:
    """
    Update a company.
    :param essentials:
    :param company_id: ID of company to update.
    :param company: HTTP request body serialized to model object.
    :param user: Current authenticated user.
    :param company_datastore: Company database access.
    :return: CompanyOutModel.
    """
    print(user.email)
    company = company_datastore.update_company(
        company.to_database_model(company_id)
    )
    return CompanyOutModel.from_database_model(
        company, essentials.language, essentials.timezone, essentials.request
    )
