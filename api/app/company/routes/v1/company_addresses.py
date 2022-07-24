from fastapi import APIRouter, Depends, Security

from app.company.datastores.address_datastore import AddressDatastore, get_address_datastore
from app.authentication.dependencies.user import get_current_user
from app.company.models.v1.addresses import AddAddressModel
from app.company.models.db.address import Address
from app.user.models.db.user import User

router = APIRouter(prefix="/v1/{lang}/companies/{company_id}/addresses", tags=["CompanyAddresses"])


@router.post("/", response_model=Address)
async def add_address(
    company_id: str,
    address: AddAddressModel,
    address_datastore: AddressDatastore = Depends(get_address_datastore),
    authenticated_user: User = Security(
        get_current_user, scopes=("roles:superuser", "roles:company_admin:{company_id}")
    ),
):
    new_address = address_datastore.add_address(company_id, address.to_database_model(), authenticated_user)
    return new_address
