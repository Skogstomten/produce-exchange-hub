"""
Routing module for company contacts.
"""
from fastapi import APIRouter, Path, Body, Depends, Security
from starlette import status

from app.datastores.company_datastore import (
    CompanyDatastore,
    get_company_datastore,
)
from app.dependencies.essentials import Essentials, get_essentials
from app.dependencies.user import get_current_user
from app.models.v1.api_models.contacts import (
    CreateContactModel,
    ContactOutModel,
    UpdateContactModel,
)
from app.models.v1.database_models.user_database_model import UserDatabaseModel

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
    company_id: str = Path(...),
    model: CreateContactModel = Body(...),
    companies: CompanyDatastore = Depends(get_company_datastore),
    user: UserDatabaseModel = Security(get_current_user, scopes=("roles:superuser", "roles:company_admin:{company_id}")),
    essentials: Essentials = Depends(get_essentials),
) -> ContactOutModel:
    """Add a contact to a company."""
    contact = companies.add_contact(company_id, model.to_database_model(user))
    return ContactOutModel.from_database_model(contact, essentials.request, essentials.timezone)


@router.put(
    "/{contact_id}",
    response_model=ContactOutModel,
    responses={
        200: {"description": "Updated successfully."},
        404: {"description": "Either company or contact was not found."},
    },
)
async def update_contact(
    company_id: str = Path(...),
    contact_id: str = Path(...),
    contact: UpdateContactModel = Body(...),
    company_datastore: CompanyDatastore = Depends(get_company_datastore),
    user: UserDatabaseModel = Security(get_current_user, scopes=("roles:superuser", "roles:company_admin:{company_id}")),
    essentials: Essentials = Depends(get_essentials),
):
    """Update contact on company."""
    contact = company_datastore.update_contact(company_id, contact.to_database_model(contact_id), user)
    return ContactOutModel.from_database_model(contact, essentials.request, essentials.timezone)


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
