"""
Has utility functions for working with datetime objects.
"""
from pytz import timezone, utc, all_timezones_set
from datetime import datetime, tzinfo


def ensure_utc(dt: datetime) -> datetime:
    """
    Makes sure datetime has timezone utc.

    ********************
    Examples
    *******************
    >>> d = ensure_utc(datetime.now())
    >>> d.tzinfo == utc
    True

    >>> d = ensure_utc(datetime.now(utc))
    >>> d.tzinfo == utc
    True

    >>> d = ensure_utc(datetime.now(timezone('Europe/Stockholm')))
    >>> d.tzinfo == utc
    True

    :param dt: the datetime object to be checked.
    :return: datetime instance of the same time but ensured to be utc timezone.
    """
    if dt.tzinfo is not None:
        if dt.tzinfo.utcoffset(dt) is not None:
            if dt.tzinfo == utc:
                return dt
    return dt.astimezone(utc)


def to_timezone(dt: datetime | None, tz: str | tzinfo) -> datetime | None:
    """
    Converts datetime object to given timezone.

    ****************
    Examples:

    >>> d = to_timezone(datetime.now(), utc)
    >>> d.tzinfo
    <UTC>

    >>> d = to_timezone(datetime.now(utc), "Europe/Stockholm")
    >>> d.tzinfo
    <DstTzInfo 'Europe/Stockholm' CEST+2:00:00 DST>

    >>> d = to_timezone(None, "utc")
    >>> d is None
    True

    >>> to_timezone(datetime.now(), "shit_timezone")
    Traceback (most recent call last):
    ...
    ValueError: Timezone name 'shit_timezone' is not a valid timezone.

    ****************
    :param dt: Original datetime object.
    :param tz: Name of the timezone to change to or tzinfo for given timezone.
        See pytz doc for available timezones.
    :return: New datetime object with requested timezone.
    """
    if dt is None:
        return None
    if isinstance(tz, str):
        if tz not in all_timezones_set:
            raise ValueError(f"Timezone name '{tz}' is not a valid timezone.")
        tz = timezone(tz)
    elif isinstance(tz, tzinfo):
        pass
    else:
        raise ValueError(f"Type '{type(tz)}'")
    if dt.tzinfo is not None:
        if dt.tzinfo.utcoffset(dt) is not None:
            if dt.tzinfo == tz:
                return dt
    return dt.astimezone(tz)
