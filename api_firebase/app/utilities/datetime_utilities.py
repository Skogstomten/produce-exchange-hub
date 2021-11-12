from datetime import datetime

import pytz


def format_datetime(value: datetime, timezone: str) -> str:
    return value.astimezone(pytz.timezone(timezone)).strftime('%Y-%m-%dT%H:%M:%S.%f%z')
