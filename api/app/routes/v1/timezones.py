"""
Route module for timezones endpoint.
"""
from pytz import all_timezones

from fastapi import APIRouter

router = APIRouter(prefix="/v1/{lang}/timezones", tags=["Timezones"])


@router.get("/", response_model=list[str])
async def get_timezones() -> list[str]:
    """
    Kind of pointless endpoint but it's mainly here for the UI to be able to
    get the available timezones instead of having to hardcode
    in the web application or something like that.
    :return: list of str with timezone names.
    """
    return all_timezones
