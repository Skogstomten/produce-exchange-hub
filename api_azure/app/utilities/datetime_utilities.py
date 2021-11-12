from datetime import datetime

import pytz

datetime_format = '%Y-%m-%dT%H:%M:%S.%f%z'


def format_datetime(value: datetime, timezone: str = 'UTC') -> str:
    return value.astimezone(pytz.timezone(timezone)).strftime(datetime_format)


def parse_datetime(value: str, timezone: pytz.tzinfo) -> datetime:
    return datetime.strptime(value, datetime_format).astimezone(timezone)
