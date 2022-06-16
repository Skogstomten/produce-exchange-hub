"""
Has utility functions for working with datetime objects.
"""
from datetime import datetime
from pytz import utc


def ensure_utc(dt: datetime) -> datetime:
    """
    Makes sure datetime has timezone utc.

    >>> d = ensure_utc(datetime.now())
    >>> d.tzinfo == utc
    True

    >>> d = ensure_utc(datetime.now(utc))
    >>> d.tzinfo == utc
    True

    >>> from pytz import timezone
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
