"""
Dependency to get timezone header.
"""
from pytz import all_timezones_set

from fastapi import Header

from app.shared.errors import UnsupportedTimezoneError


def get_timezone_header(timezone: str = Header("Europe/Stockholm")) -> str:
    """
    Get timezone header or default value.

    Default Value="Europe/Stockholm".
    :raise UnsupportedTimezoneError: If timezone is not in the list of
    supported timezones in the pytz library.
    :param timezone: Timezone as str. Taken from HTTP header with same name.
    :return: Timezone name.
    """
    if timezone not in all_timezones_set:
        raise UnsupportedTimezoneError(timezone)
    return timezone
