"""
Routing module for company contacts.
"""
from fastapi import APIRouter, Path, Body, Request, Depends

from app.dependencies.user import get_current_user
from app.models.v1.database_models.user_database_model import UserDatabaseModel
from app.models.v1.api_models.contacts import (
    CreateContactModel,
    ContactOutModel,
)
from app.datastores.company_datastore import (
    CompanyDatastore,
    get_company_datastore,
)


router = APIRouter(
    prefix="/v1/{lang}/companies/{company_id}/contacts",
    tags=["CompanyContacts"],
)


@router.post("/", response_model=ContactOutModel)
def add_contact(
    request: Request,
    company_id: str = Path(...),
    model: CreateContactModel = Body(...),
    companies: CompanyDatastore = Depends(get_company_datastore),
    user: UserDatabaseModel = Depends(get_current_user),
) -> ContactOutModel:
    """
    Add a contact to a company.
    :param request: http request object.
    :param company_id: id of the company to add the contact too.
    :param model:
    :param companies:
    :param user:
    :return:
    """
    print(user.email)
    contact = companies.add_contact_to_company(company_id, model.to_database_model())
    return ContactOutModel.from_database_model(contact, request)
