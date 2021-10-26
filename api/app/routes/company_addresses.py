from fastapi import APIRouter, Depends, Path, Body

from app.datastores.addresses_datastore import AddressesDatastore, get_addresses_datastore
from app.dependencies.app_headers import AppHeaders, get_headers
from app.models.api_list_response_model import ApiListResponseModel
from app.models.companies.addresses.addresses_put_model import AddressesPutModel
from app.models.companies.in_models.company_post_put_model import AddressPostPutModel
from app.models.companies.out_models.address_out_model import AddressOutModel

router = APIRouter(prefix='/companies/{company_id}/addresses')


@router.get('/', response_model=ApiListResponseModel[AddressOutModel])
def get_addresses(
        headers: AppHeaders = Depends(get_headers),
        company_id: str = Path(...),
        datastore: AddressesDatastore = Depends(get_addresses_datastore)
):
    addresses = datastore.get_addresses(company_id, headers)
    return ApiListResponseModel(addresses)


@router.post('/', response_model=ApiListResponseModel[AddressOutModel])
def add_address(
        headers: AppHeaders = Depends(get_headers),
        company_id: str = Path(...),
        body: AddressPostPutModel = Body(...),
        datastore: AddressesDatastore = Depends(get_addresses_datastore)
):
    addresses = datastore.add_address(company_id, body, headers)
    return ApiListResponseModel(addresses)


@router.put('/', response_model=ApiListResponseModel[AddressOutModel])
def update_addresses(
        headers: AppHeaders = Depends(get_headers),
        company_id: str = Path(...),
        body: AddressesPutModel = Body(...),
        datastore: AddressesDatastore = Depends(get_addresses_datastore)
):
    addresses = datastore.update_addresses(company_id, body.addresses, headers)
    return ApiListResponseModel(addresses)
