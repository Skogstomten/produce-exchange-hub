"""
Routing module for companies endpoint.
"""
from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Body, Path, Security, File, UploadFile, Request
from fastapi.responses import PlainTextResponse, FileResponse
from pytz import utc

from app.authentication.dependencies.user import get_current_user, get_current_user_if_any
from app.company.models.shared.enums import SortOrder
from app.company.models.v1.company_api_models import (
    CompanyOutModel,
    CompanyCreateModel,
    CompanyUpdateForm,
    CompanyOutListModel,
)
from app.company.models.v1.paging_information import (
    PagingInformation,
    get_paging_information,
)
from app.database.enums import CompanyStatus
from app.database.models import User, Company
from app.logging.log import AppLoggerInjector, AppLogger
from app.shared.config.routing_config import BASE_PATH
from app.shared.dependencies.request_context import RequestContext, get_request_context
from app.shared.io.file_manager import FileManager, get_file_manager
from app.shared.models.v1.paging_response_model import PagingResponseModel
from app.shared.utils.request_utils import get_url
from app.shared.utils.url_utils import assemble_profile_picture_url

logger_injector = AppLoggerInjector("companies_router")

router = APIRouter(prefix=BASE_PATH + "/companies", tags=["Companies"])


@router.get("/", response_model=PagingResponseModel[CompanyOutListModel])
async def get_companies(
    sort_by: str | None = Query(None),
    sort_order: SortOrder = Query(SortOrder.asc),
    context: RequestContext = Depends(get_request_context),
    paging_information: PagingInformation = Depends(get_paging_information),
    authenticated_user: User | None = Depends(get_current_user_if_any),
    logger: AppLogger = Depends(logger_injector),
) -> PagingResponseModel[CompanyOutListModel]:
    """Get list of companies wrapped in a paging response."""
    logger.debug(
        f"Incoming={get_url(context.request)}: sort_by={sort_by}, sort_order={sort_order}, "
        f"essentials={context}, paging_information={paging_information}, user={authenticated_user}"
    )

    query = Company.select()
    if sort_by is not None:
        match sort_by:
            case "name":
                query = query.order_by(Company.name.asc() if sort_order == SortOrder.desc else Company.name.desc())
            case "status":
                query = query.order_by(Company.status.asc() if sort_order == SortOrder.asc else Company.status.desc())
            case "created_date":
                query = query.order_by(
                    Company.created_date.asc() if sort_order == SortOrder.asc else Company.created_date.desc()
                )
            case "company_types":
                query = query.order_by(
                    Company.company_types.asc() if sort_order == SortOrder.asc else Company.company_types.desc()
                )
            case "content_language":
                query = query.order_by(
                    Company.content_languages_iso.asc()
                    if sort_order == SortOrder.asc
                    else Company.content_languages_iso.desc()
                )
            case "activation_date":
                query = query.order_by(
                    Company.activation_date.asc() if sort_order == SortOrder.asc else Company.activation_date.desc()
                )

    query = query.paginate(paging_information.page, paging_information.page_size)

    items: list[CompanyOutListModel] = []
    for company in query:
        item = CompanyOutListModel.from_database_model(
            company, context.language, context.timezone, context.request, router, None
        )
        items.append(item)
    response = PagingResponseModel[CompanyOutListModel].create(
        items,
        paging_information.page,
        paging_information.page_size,
        context.request,
    )
    return response


@router.get("/{company_id}", response_model=CompanyOutModel)
async def get_company(
    company_id: UUID,
    essentials: RequestContext = Depends(get_request_context),
    authenticated_user: User = Depends(get_current_user_if_any),
) -> CompanyOutModel:
    """Get a company by id."""
    company = Company.get_by_id(company_id)
    return CompanyOutModel.from_database_model(
        company,
        essentials.language,
        essentials.timezone,
        essentials.request,
        router,
        company.changes if authenticated_user.is_superuser or authenticated_user.is_company_admin(company_id) else None,
    )


@router.post("/", response_model=CompanyOutModel)
async def add_company(
    company: CompanyCreateModel = Body(...),
    authenticated_user: User = Security(get_current_user, scopes=("verified:True",)),
    context: RequestContext = Depends(get_request_context),
) -> CompanyOutModel:
    """Add a new company."""
    company = Company(**company.model_dump())
    company.save()
    company.users.add(authenticated_user)
    company.save()
    return CompanyOutModel.from_database_model(
        company, context.language, context.timezone, context.request, router, None
    )


@router.put("/{company_id}", response_model=CompanyOutModel)
async def update_company(
    company_id: str = Path(...),
    form_data: CompanyUpdateForm = Body(...),
    authenticated_user: User = Security(
        get_current_user,
        scopes=("roles:company_admin:{company_id}",),
    ),
    essentials: RequestContext = Depends(get_request_context),
):
    """Update a company."""
    company = Company.get_by_id(company_id)
    company.name = form_data.name
    company.company_types = form_data.company_types
    company.content_languages_iso = form_data.content_languages_iso
    company.external_website_url = form_data.external_website_url
    company.save()

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
    essenties: RequestContext = Depends(get_request_context),
) -> CompanyOutModel:
    """Activates new company."""
    company = Company.get_by_id(company_id)
    company.status = CompanyStatus.active
    company.activation_date = datetime.now(utc)
    company.save()
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
    essentials: RequestContext = Depends(get_request_context),
):
    """Deactivates a company."""
    company = Company.get_by_id(company_id)
    company.status = CompanyStatus.deactivated
    company.save()
    return CompanyOutModel.from_database_model(
        company, essentials.language, essentials.timezone, essentials.request, router, authenticated_user
    )


@router.get("/{company_id}/descriptions", response_model=dict[str, str])
async def get_company_descriptions(
    company_id: str,
    user: User = Security(get_current_user, scopes=("roles:superuser", "roles:company_admin:{company_id}")),
    logger: AppLogger = Depends(logger_injector),
):
    logger.debug(f"Call from user {user}")
    company = Company.get_by_id(company_id)
    return company.description


@router.put("/{company_id}/descriptions", response_model=CompanyOutModel)
async def update_company_descriptions(
    company_id: str,
    descriptions: dict[str, str] = Body(...),
    authenticated_user: User = Security(
        get_current_user, scopes=("roles:superuser", "roles:company_admin:{company_id}")
    ),
    essentials: RequestContext = Depends(get_request_context),
):
    """
    Updated description for company. Can receive multiple translations.
    """
    company = Company.get_by_id(company_id)
    company.description = descriptions
    company.save()

    return CompanyOutModel.from_database_model(
        company,
        essentials.language,
        essentials.timezone,
        essentials.request,
        router,
        authenticated_user,
    )


@router.post("/{company_id}/profile-pictures", response_class=PlainTextResponse)
async def upload_profile_picture(
    company_id: str,
    file: UploadFile = File(...),
    user: User = Security(get_current_user, scopes=("roles:superuser", "roles:company_admin:{company_id}")),
    context: RequestContext = Depends(get_request_context),
    file_manager: FileManager = Depends(get_file_manager),
    logger: AppLogger = Depends(logger_injector),
):
    logger.debug(f"Upload_profile_picture called by {user}")
    company = Company.get_by_id(company_id)
    company.profile_picture_file_name = await file_manager.save_company_profile_picture(company_id, file)
    company.save()
    return assemble_profile_picture_url(context.request, router, company.profile_picture_file_name, context.language)


@router.get("/profile-pictures/{image_file_name}", response_class=FileResponse)
async def get_profile_picture(
    request: Request,
    image_file_name: str,
    logger: AppLogger = Depends(logger_injector),
    file_manager: FileManager = Depends(get_file_manager),
):
    logger.debug(f"Incoming={get_url(request)}")
    return file_manager.get_company_profile_picture_physical_path(image_file_name)
