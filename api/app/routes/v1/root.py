from fastapi import APIRouter, Depends

from app.dependencies.user import get_current_user_if_any
from app.models.v1.database_models.user_database_model import UserDatabaseModel
from app.models.v1.root import Root

router = APIRouter(tags=["Root"])


@router.get("/v1", response_model=Root)
async def root(
    user: UserDatabaseModel | None = Depends(get_current_user_if_any),
):
    result = {}
    if user is not None:
        result["current_user"] = user.email
    return result
