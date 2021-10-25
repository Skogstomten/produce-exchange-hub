from datetime import datetime

import pytz


def format_datetime(value: datetime, timezone: str) -> str:
    return value.astimezone(pytz.timezone(timezone)).strftime('%Y-%m-%d %H:%M:%S.%f %z')
