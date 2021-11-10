from fastapi import APIRouter, Path, Depends

from ..models.users.user_out_model import UserOutModel
from ..datastores.users_datastore import UsersDatastore, get_users_datastore

router = APIRouter(
    prefix='/users'
)


@router.get('/{user_id}', response_model=UserOutModel)
def get_user(
        user_id: str = Path(...),
        datastore: UsersDatastore = Depends(get_users_datastore),
):
    return datastore.get_user(user_id)
