import pytz

from fastapi import Header


def get_timezone_header(
        timezone: str = Header('Europe/Stockholm')
) -> str:
    if timezone not in pytz.all_timezones_set:
        raise UnsupportedTimezoneError(timezone)
    return timezone
