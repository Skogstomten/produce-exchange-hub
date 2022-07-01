"""
Routing module for company contacts.
"""
from fastapi import APIRouter, Path, Body, Request, Depends, Security
from starlette import status

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


@router.post(
    "/",
    response_model=ContactOutModel,
    status_code=status.HTTP_201_CREATED,
    responses={201: {"description": "Contact has been created", "model": ContactOutModel}},
)
async def add_contact(
    request: Request,
    company_id: str = Path(...),
    model: CreateContactModel = Body(...),
    companies: CompanyDatastore = Depends(get_company_datastore),
    user: UserDatabaseModel = Security(get_current_user, scopes=("roles:superuser", "roles:company_admin:{company_id}")),
) -> ContactOutModel:
    """Add a contact to a company."""
    contact = companies.add_contact(company_id, model.to_database_model(user))
    return ContactOutModel.from_database_model(contact, request)


@router.delete(
    "/{contact_id}", status_code=status.HTTP_204_NO_CONTENT, responses={204: {"description": "Contact has been deleted"}}
)
async def delete_contact(
    contact_id: str = Path(...),
    company_id: str = Path(...),
    company_datastore: CompanyDatastore = Depends(get_company_datastore),
    user: UserDatabaseModel = Security(get_current_user, scopes=("roles:superuser", "roles:company_admin:{company_id}")),
) -> None:
    """Delete contact from company."""
    company_datastore.delete_contact(company_id, contact_id, user)
