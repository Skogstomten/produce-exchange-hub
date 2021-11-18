# from fastapi import APIRouter, Depends, Path, Body
#
# from app.datastores.addresses_datastore import AddressesDatastore, get_addresses_datastore
# from app.dependencies.app_headers import AppHeaders, get_headers
# from app.models.api_list_response_model import ApiListResponseModel
#
# from app.models.companies.addresses.address_in_model import AddressInModel
# from app.models.companies.addresses.address_out_model import AddressOutModel
#
# router = APIRouter(prefix='/companies/{company_id}/addresses')
#
#
# @router.get('/', response_model=ApiListResponseModel[AddressOutModel])
# def get_addresses(
#         headers: AppHeaders = Depends(get_headers),
#         company_id: str = Path(...),
#         datastore: AddressesDatastore = Depends(get_addresses_datastore)
# ):
#     addresses = datastore.get_addresses(company_id, headers)
#     return ApiListResponseModel.create(addresses)
#
#
# @router.get('/{address_id}', response_model=AddressOutModel)
# def get_address(
#         headers: AppHeaders = Depends(get_headers),
#         company_id: str = Path(...),
#         address_id: str = Path(...),
#         datastore: AddressesDatastore = Depends(get_addresses_datastore)
# ):
#     return datastore.get_address(company_id, address_id, headers)
#
#
# @router.post('/', response_model=AddressOutModel)
# def add_address(
#         headers: AppHeaders = Depends(get_headers),
#         company_id: str = Path(...),
#         body: AddressInModel = Body(...),
#         datastore: AddressesDatastore = Depends(get_addresses_datastore)
# ):
#     return datastore.add_address(company_id, body, headers)
#
#
# @router.put('/', response_model=AddressOutModel)
# def update_address(
#         headers: AppHeaders = Depends(get_headers),
#         company_id: str = Path(...),
#         address_id: str = Path(...),
#         body: AddressInModel = Body(...),
#         datastore: AddressesDatastore = Depends(get_addresses_datastore)
# ):
#     return datastore.update_address(company_id, address_id, body, headers)
