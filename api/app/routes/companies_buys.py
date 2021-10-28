from fastapi import APIRouter, Depends, Body, Path, Header

from ..datastores.buys_datastore import BuysOutModel, BuysInModel, BuysDatastore, get_buys_datastore
from ..models.api_list_response_model import ApiListResponseModel
from ..dependencies.app_headers import AppHeaders, get_headers

router = APIRouter(prefix='/companies/{company_id}/buys')


@router.get('/', response_model=ApiListResponseModel[BuysOutModel])
def get_all(
        headers: AppHeaders = Depends(get_headers),
        company_id: str = Path(...),
        datastore: BuysDatastore = Depends(get_buys_datastore)
):
    buys = datastore.get_buys(company_id, headers)
    return ApiListResponseModel.create(buys)


@router.get('/{buys_id}', response_model=BuysOutModel)
def get(
        headers: AppHeaders = Depends(get_headers),
        company_id: str = Path(...),
        buys_id: str = Path(...),
        datastore: BuysDatastore = Depends(get_buys_datastore)
):
    return datastore.get_buys_post(company_id, buys_id, headers)
