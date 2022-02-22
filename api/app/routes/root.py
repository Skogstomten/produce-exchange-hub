from fastapi import APIRouter, Depends

from ..dependencies.user import get_current_user_if_any
from ..models.user import UserInternal
from ..models.root import Root

router = APIRouter()


@router.get('/', response_model=Root)
async def root(
        user: UserInternal | None = Depends(get_current_user_if_any)
):
    result = {}
    if user is not None:
        result['current_user'] = user.email
    return result
