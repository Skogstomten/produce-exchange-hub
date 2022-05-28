from fastapi import APIRouter, Depends, Request, Query

from ...models.v1.api_models.output_list import OutputListModel
from ...datastores.user_datastore import UserDatastore, get_user_datastore

router = APIRouter(prefix='/v1/{lang}/claims')


@router.get('/', response_model=OutputListModel[str])
async def get_claims(
        request: Request,
        users: UserDatastore = Depends(get_user_datastore),
        offset: int = Query(0),
        size: int = Query(20),
):
    users = users.get_claims()
    items: list = [user.claim_type for user in users]
    return OutputListModel[str].create(items, len(items), offset, size, request)
