"""
Routing module for companies endpoint.
"""
from fastapi import APIRouter, Depends, Query, Body, Path, Security, File, UploadFile
from fastapi.responses import PlainTextResponse, FileResponse
from starlette import status
from starlette.requests import Request

from app.datastores.company_datastore import (
    CompanyDatastore,
    get_company_datastore,
)
from app.dependencies.essentials import Essentials, get_essentials
from app.dependencies.log import AppLoggerInjector, AppLogger
from app.dependencies.paging_information import (
    PagingInformation,
    get_paging_information,
)
from app.dependencies.user import get_current_user, get_current_user_if_any
from app.errors import ErrorModel
from app.models.v1.api_models.companies import (
    CompanyOutModel,
    CompanyCreateModel,
    CompanyUpdateModel,
    CompanyOutListModel, assemble_company_profile_picture_url,
)
from app.models.v1.api_models.paging_response_model import PagingResponseModel
from app.models.v1.database_models.user_database_model import UserDatabaseModel
from app.models.v1.shared import SortOrder
from app.utils.request_utils import get_url

logger_injector = AppLoggerInjector("companies_router")

router = APIRouter(prefix="/v1/{lang}/companies", tags=["Companies"])


@router.get("/", response_model=PagingResponseModel[CompanyOutListModel])
async def get_companies(
    sort_by: str | None = Query(None),
    sort_order: SortOrder = Query(SortOrder.asc),
    company_datastore: CompanyDatastore = Depends(get_company_datastore),
    essentials: Essentials = Depends(get_essentials),
    paging_information: PagingInformation = Depends(get_paging_information),
    user: UserDatabaseModel = Depends(get_current_user_if_any),
    logger: AppLogger = Depends(logger_injector),
) -> PagingResponseModel[CompanyOutListModel]:
    """Get list of companies wrapped in a paging response."""
    logger.debug(
        f"Incoming={get_url(essentials.request)}: sort_by={sort_by}, sort_order={sort_order}, "
        f"essentials={essentials}, paging_information={paging_information}, user={user}"
    )
    company_datastore = company_datastore.get_companies(
        paging_information.skip, paging_information.take, sort_by, sort_order, user
    )
    items: list[CompanyOutListModel] = []
    for company in company_datastore:
        item = CompanyOutListModel.from_database_model(
            company,
            essentials.language,
            essentials.timezone,
            essentials.request,
            router.prefix,
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
    company_id: str = Path(...),
    company_datastore: CompanyDatastore = Depends(get_company_datastore),
    essentials: Essentials = Depends(get_essentials),
    user: UserDatabaseModel = Depends(get_current_user_if_any),
) -> CompanyOutModel:
    """Get a company by id."""
    company = company_datastore.get_company(company_id, user)
    return CompanyOutModel.from_database_model(
        company, essentials.language, essentials.timezone, essentials.request, router.prefix
    )


@router.post("/", response_model=CompanyOutModel)
async def add_company(
    company: CompanyCreateModel = Body(...),
    user: UserDatabaseModel = Security(get_current_user, scopes=("verified:True",)),
    company_datastore: CompanyDatastore = Depends(get_company_datastore),
    essentials: Essentials = Depends(get_essentials),
) -> CompanyOutModel:
    """Add a new company."""
    company = company_datastore.add_company(company, user)
    return CompanyOutModel.from_database_model(
        company, essentials.language, essentials.timezone, essentials.request, router.prefix
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
):
    """Update a company."""
    company = company_datastore.update_company(company_id, company, user)
    return CompanyOutModel.from_database_model(
        company, essentials.language, essentials.timezone, essentials.request, router.prefix
    )


@router.put("/{company_id}/activate", response_model=CompanyOutModel)
async def activate_company(
    company_id: str = Path(...),
    user: UserDatabaseModel = Security(
        get_current_user,
        scopes=(
            "roles:superuser",
            "roles:company_admin:{company_id}",
        ),
    ),
    company_datastore: CompanyDatastore = Depends(get_company_datastore),
    essenties: Essentials = Depends(get_essentials),
) -> CompanyOutModel:
    """Activates new company."""
    company = company_datastore.activate_company(company_id, user)
    return CompanyOutModel.from_database_model(
        company, essenties.language, essenties.timezone, essenties.request, router.prefix
    )


@router.get(
    "/{company_id}/names",
    response_model=dict[str, str],
    responses={
        status.HTTP_200_OK: {
            "description": "Successful response.",
            "content": {
                "application/json": {
                    "example": {
                        "sv": "Firmanamn",
                        "en": "Company name",
                    }
                }
            },
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Company not found.",
            "model": ErrorModel,
            "content": {
                "application/json": {
                    "example": ErrorModel.create(status.HTTP_404_NOT_FOUND, "Company not found", "this:is/url").dict()
                }
            },
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Internal Server Error",
            "model": ErrorModel,
            "content": {
                "application/json": {
                    "example": ErrorModel.create(
                        status.HTTP_500_INTERNAL_SERVER_ERROR, "Someone shat in the blue locker", "this:is/url"
                    ).dict()
                }
            },
        },
    },
)
async def get_company_names(
    request: Request,
    company_id: str,
    user: UserDatabaseModel = Security(
        get_current_user,
        scopes=("roles:superuser", "roles:company_admin:{company_id}"),
    ),
    company_datastore: CompanyDatastore = Depends(get_company_datastore),
    logger: AppLogger = Depends(logger_injector),
):
    """Get the map of names for company for easy edit and update."""
    logger.debug(f"Incoming={get_url(request)}: company_id={company_id}, user={user}")
    company = company_datastore.get_company(company_id, user)
    return company.name


@router.put("/{company_id}/names", response_model=CompanyOutModel)
async def update_company_names(
    company_id: str,
    names: dict[str, str] = Body(...),
    user: UserDatabaseModel = Security(get_current_user, scopes=("roles:superuser", "roles:company_admin:{company_id}")),
    company_datastore: CompanyDatastore = Depends(get_company_datastore),
    essentials: Essentials = Depends(get_essentials),
):
    company = company_datastore.update_company_names(company_id, names, user)
    return CompanyOutModel.from_database_model(
        company, essentials.language, essentials.timezone, essentials.request, router.prefix
    )


@router.get("/{company_id}/descriptions", response_model=dict[str, str])
async def get_company_descriptions(
    company_id: str,
    user: UserDatabaseModel = Security(get_current_user, scopes=("roles:superuser", "roles:company_admin:{company_id}")),
    company_datastore: CompanyDatastore = Depends(get_company_datastore),
):
    company = company_datastore.get_company(company_id, user)
    return company.description


@router.put("/{company_id}/descriptions", response_model=CompanyOutModel)
async def update_company_descriptions(
    company_id: str,
    descriptions: dict[str, str] = Body(...),
    user: UserDatabaseModel = Security(get_current_user, scopes=("roles:superuser", "roles:company_admin:{company_id}")),
    company_datastore: CompanyDatastore = Depends(get_company_datastore),
    essentials: Essentials = Depends(get_essentials),
):
    company = company_datastore.update_company_descriptions(company_id, descriptions, user)
    return CompanyOutModel.from_database_model(
        company, essentials.language, essentials.timezone, essentials.request, router.prefix
    )


@router.post("/{company_id}/profile-pictures", response_class=PlainTextResponse)
async def upload_profile_picture(
    company_id: str,
    file: UploadFile = File(...),
    company_datastore: CompanyDatastore = Depends(get_company_datastore),
    user: UserDatabaseModel = Security(
        get_current_user,
        scopes=("roles:superuser", "roles:company_admin:{company_id}"),
    ),
    essentials: Essentials = Depends(get_essentials),
):
    file_path = await company_datastore.save_profile_picture(company_id, file, user)
    return assemble_company_profile_picture_url(essentials.request, router.prefix, file_path, essentials.language)


@router.get("/profile-pictures/{image_file_name}", response_class=FileResponse)
async def get_profile_picture(
    request: Request,
    image_file_name: str,
    company_datastore: CompanyDatastore = Depends(get_company_datastore),
    logger: AppLogger = Depends(logger_injector),
):
    logger.debug(f"Incoming={get_url(request)}")
    return company_datastore.get_company_profile_picture_physical_path(image_file_name)
