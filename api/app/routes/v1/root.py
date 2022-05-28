from fastapi import APIRouter, Depends

from app.dependencies.user import get_current_user_if_any
from app.models.v1.users import UserInternal
from app.models.v1.root import Root

router = APIRouter()


@router.get('/v1', response_model=Root)
async def root(
        user: UserInternal | None = Depends(get_current_user_if_any)
):
    result = {}
    if user is not None:
        result['current_user'] = user.email
    return result
