from datetime import datetime

import pytz


def format_datetime(value: datetime | None, timezone: str) -> str | None:
    if value is None:
        return None
    return value.astimezone(pytz.timezone(timezone)).strftime('%Y-%m-%dT%H:%M:%S.%f%z')
