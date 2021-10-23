from datetime import datetime
import pytz


def format_date(dt: datetime, timezone_name: str) -> str:
    timezone = pytz.timezone(timezone_name)
    return dt.astimezone(timezone).strftime('%Y-%m-%d %H:%M:%S.%f %z')
