"""
Routing module for company contacts.
"""
from fastapi import APIRouter, Path, Body, Depends, Security, status

from app.company.datastores.company_datastore import (
    CompanyDatastore,
    get_company_datastore,
)
from app.shared.dependencies.essentials import Essentials, get_essentials
from app.authentication.dependencies.user import get_current_user
from app.company.models.v1.contacts import (
    AddContactModel,
    ContactOutModel,
    UpdateContactModel,
)
from app.authentication.models.db.user import User

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
    model: AddContactModel = Body(...),
    companies: CompanyDatastore = Depends(get_company_datastore),
    authenticated_user: User = Security(get_current_user, scopes=("roles:company_admin:{company_id}",)),
    essentials: Essentials = Depends(get_essentials),
) -> ContactOutModel:
    """Add a contact to a company."""
    contact = companies.add_contact(company_id, model, authenticated_user)
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
    user: User = Security(get_current_user, scopes=("roles:superuser", "roles:company_admin:{company_id}")),
    essentials: Essentials = Depends(get_essentials),
):
    """Update contact on company."""
    contact = company_datastore.update_contact(company_id, contact_id, contact, user)
    return ContactOutModel.from_database_model(contact, essentials.request, essentials.timezone)


@router.delete(
    "/{contact_id}", status_code=status.HTTP_204_NO_CONTENT, responses={204: {"description": "Contact has been deleted"}}
)
async def delete_contact(
    contact_id: str = Path(...),
    company_id: str = Path(...),
    company_datastore: CompanyDatastore = Depends(get_company_datastore),
    user: User = Security(get_current_user, scopes=("roles:superuser", "roles:company_admin:{company_id}")),
) -> None:
    """Delete contact from company."""
    company_datastore.delete_contact(company_id, contact_id, user)
