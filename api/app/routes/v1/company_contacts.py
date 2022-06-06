from fastapi import APIRouter, Path, Body, Request, Depends

from app.dependencies.timezone_header import get_timezone_header
from app.dependencies.user import get_current_user
from app.models.v1.shared import Language
from app.models.v1.users import UserInternal
from app.models.v1.api_models.companies import ContactModel
from app.datastores.company_datastore import CompanyDatastore, get_company_datastore


router = APIRouter(prefix='/v1/{lang}/companies/{company_id}/contacts')


@router.post('/', response_model=ContactModel)
def add_contact(
        request: Request,
        lang: Language = Path(...),
        company_id: str = Path(...),
        model: ContactModel = Body(...),
        timezone: str = Depends(get_timezone_header),
        companies: CompanyDatastore = Depends(get_company_datastore),
        user: UserInternal = Depends(get_current_user)
):
    contact = companies.add_contact_to_company(company_id, model, user)
    return ContactModel.from_database_model(contact)
