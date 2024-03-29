"""
Routing module for companies endpoint.
"""
from fastapi import APIRouter, Depends, Query, Body, Path, Security, File, UploadFile, status, Request
from fastapi.responses import PlainTextResponse, FileResponse

from app.company.datastores.company_datastore import (
    CompanyDatastore,
    get_company_datastore,
)
from app.company.datastores.company_profile_picture_datastore import (
    get_company_profile_picture_datastore,
    CompanyProfilePictureDatastore,
)
from app.company.datastores.company_user_datastore import CompanyUserDatastore, get_company_user_datastore
from app.company.models.shared.enums import SortOrder
from app.shared.config.routing_config import BASE_PATH
from app.shared.dependencies.essentials import Essentials, get_essentials
from app.logging.log import AppLoggerInjector, AppLogger
from app.company.models.v1.paging_information import (
    PagingInformation,
    get_paging_information,
)
from app.authentication.dependencies.user import get_current_user, get_current_user_if_any
from app.shared.errors.errors import ErrorModel
from app.company.models.v1.company_api_models import (
    CompanyOutModel,
    CompanyCreateModel,
    CompanyUpdateModel,
    CompanyOutListModel,
)
from app.shared.models.v1.paging_response_model import PagingResponseModel
from app.authentication.models.db.user import User
from app.shared.utils.request_utils import get_url
from app.shared.utils.url_utils import assemble_profile_picture_url

logger_injector = AppLoggerInjector("companies_router")

router = APIRouter(prefix=BASE_PATH + "/companies", tags=["Companies"])


@router.get("/", response_model=PagingResponseModel[CompanyOutListModel])
async def get_companies(
    sort_by: str | None = Query(None),
    sort_order: SortOrder = Query(SortOrder.asc),
    company_datastore: CompanyDatastore = Depends(get_company_datastore),
    essentials: Essentials = Depends(get_essentials),
    paging_information: PagingInformation = Depends(get_paging_information),
    authenticated_user: User | None = Depends(get_current_user_if_any),
    logger: AppLogger = Depends(logger_injector),
) -> PagingResponseModel[CompanyOutListModel]:
    """Get list of companies wrapped in a paging response."""
    logger.debug(
        f"Incoming={get_url(essentials.request)}: sort_by={sort_by}, sort_order={sort_order}, "
        f"essentials={essentials}, paging_information={paging_information}, user={authenticated_user}"
    )
    company_datastore = company_datastore.get_companies(
        paging_information.skip, paging_information.take, sort_by, sort_order, authenticated_user
    )
    items: list[CompanyOutListModel] = []
    for company in company_datastore:
        item = CompanyOutListModel.from_database_model(
            company, essentials.language, essentials.timezone, essentials.request, router, authenticated_user
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
    company_id: str,
    company_datastore: CompanyDatastore = Depends(get_company_datastore),
    essentials: Essentials = Depends(get_essentials),
    authenticated_user: User = Depends(get_current_user_if_any),
) -> CompanyOutModel:
    """Get a company by id."""
    company = company_datastore.get_company(company_id, authenticated_user)
    return CompanyOutModel.from_database_model(
        company, essentials.language, essentials.timezone, essentials.request, router, authenticated_user
    )


@router.post("/", response_model=CompanyOutModel)
async def add_company(
    company: CompanyCreateModel = Body(...),
    authenticated_user: User = Security(get_current_user, scopes=("verified:True",)),
    company_datastore: CompanyDatastore = Depends(get_company_datastore),
    company_user_datastore: CompanyUserDatastore = Depends(get_company_user_datastore),
    essentials: Essentials = Depends(get_essentials),
) -> CompanyOutModel:
    """Add a new company."""
    created_company = company_datastore.add_company(company, authenticated_user)
    company_user_datastore.add_user_to_company(
        created_company.id, "company_admin", authenticated_user.id, authenticated_user
    )
    return CompanyOutModel.from_database_model(
        created_company, essentials.language, essentials.timezone, essentials.request, router, authenticated_user
    )


@router.put("/{company_id}", response_model=CompanyOutModel)
async def update_company(
    company_id: str = Path(...),
    company: CompanyUpdateModel = Body(...),
    authenticated_user: User = Security(
        get_current_user,
        scopes=("roles:company_admin:{company_id}",),
    ),
    company_datastore: CompanyDatastore = Depends(get_company_datastore),
    essentials: Essentials = Depends(get_essentials),
):
    """Update a company."""
    company = company_datastore.update_company(company_id, company, authenticated_user)
    return CompanyOutModel.from_database_model(
        company, essentials.language, essentials.timezone, essentials.request, router, authenticated_user
    )


@router.post("/{company_id}/activate", response_model=CompanyOutModel)
async def activate_company(
    company_id: str = Path(...),
    authenticated_user: User = Security(
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
    company = company_datastore.activate_company(company_id, authenticated_user)
    return CompanyOutModel.from_database_model(
        company, essenties.language, essenties.timezone, essenties.request, router, authenticated_user
    )


@router.post("/{company_id}/deactivate", response_model=CompanyOutModel)
async def deactivate_company(
    company_id: str,
    authenticated_user: User = Security(
        get_current_user,
        scopes=(
            "roles:superuser",
            "roles:company_admin:{company_id}",
        ),
    ),
    company_datastore: CompanyDatastore = Depends(get_company_datastore),
    essentials: Essentials = Depends(get_essentials),
):
    """Deactivates a company."""
    company = company_datastore.deactivate_company(company_id, authenticated_user)
    return CompanyOutModel.from_database_model(
        company, essentials.language, essentials.timezone, essentials.request, router, authenticated_user
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
    user: User = Security(
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
    authenticated_user: User = Security(
        get_current_user, scopes=("roles:superuser", "roles:company_admin:{company_id}")
    ),
    company_datastore: CompanyDatastore = Depends(get_company_datastore),
    essentials: Essentials = Depends(get_essentials),
):
    company = company_datastore.update_company_names(company_id, names, authenticated_user)
    return CompanyOutModel.from_database_model(
        company, essentials.language, essentials.timezone, essentials.request, router, authenticated_user
    )


@router.get("/{company_id}/descriptions", response_model=dict[str, str])
async def get_company_descriptions(
    company_id: str,
    user: User = Security(get_current_user, scopes=("roles:superuser", "roles:company_admin:{company_id}")),
    company_datastore: CompanyDatastore = Depends(get_company_datastore),
):
    company = company_datastore.get_company(company_id, user)
    return company.description


@router.put("/{company_id}/descriptions", response_model=CompanyOutModel)
async def update_company_descriptions(
    company_id: str,
    descriptions: dict[str, str] = Body(...),
    authenticated_user: User = Security(
        get_current_user, scopes=("roles:superuser", "roles:company_admin:{company_id}")
    ),
    company_datastore: CompanyDatastore = Depends(get_company_datastore),
    essentials: Essentials = Depends(get_essentials),
):
    company = company_datastore.update_company_descriptions(company_id, descriptions, authenticated_user)
    return CompanyOutModel.from_database_model(
        company, essentials.language, essentials.timezone, essentials.request, router, authenticated_user
    )


@router.post("/{company_id}/profile-pictures", response_class=PlainTextResponse)
async def upload_profile_picture(
    company_id: str,
    file: UploadFile = File(...),
    company_profile_picture_datastore: CompanyProfilePictureDatastore = Depends(get_company_profile_picture_datastore),
    user: User = Security(
        get_current_user,
        scopes=("roles:superuser", "roles:company_admin:{company_id}"),
    ),
    essentials: Essentials = Depends(get_essentials),
):
    file_path = await company_profile_picture_datastore.save_profile_picture(company_id, file, user)
    return assemble_profile_picture_url(essentials.request, router, file_path, essentials.language)


@router.get("/profile-pictures/{image_file_name}", response_class=FileResponse)
async def get_profile_picture(
    request: Request,
    image_file_name: str,
    company_profile_picture_datastore: CompanyProfilePictureDatastore = Depends(get_company_profile_picture_datastore),
    logger: AppLogger = Depends(logger_injector),
):
    logger.debug(f"Incoming={get_url(request)}")
    return company_profile_picture_datastore.get_company_profile_picture_physical_path(image_file_name)
