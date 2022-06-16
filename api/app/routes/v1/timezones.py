from pytz import all_timezones

from fastapi import APIRouter

router = APIRouter(prefix="/v1/{lang}/timezones", tags=["Timezones"])


@router.get("/", response_model=list[str])
async def get_timezones():
    return all_timezones
