from pytz import all_timezones_set

from fastapi import Header

from app.errors.unsupported_timezone_error import UnsupportedTimezoneError


def get_timezone_header(timezone: str = Header("Europe/Stockholm")) -> str:
    if timezone not in all_timezones_set:
        raise UnsupportedTimezoneError(timezone)
    return timezone
