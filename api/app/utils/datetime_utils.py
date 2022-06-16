"""
Has utility functions for working with datetime objects.
"""
from datetime import datetime
from pytz import utc, timezone


def ensure_utc(date: datetime) -> datetime:
    """
    Makes sure datetime has timezone utc.

    >>> d = ensure_utc(datetime.now())
    >>> d.tzinfo == utc
    True

    >>> d = ensure_utc(datetime.now(utc))
    >>> d.tzinfo == utc
    True

    >>> d = ensure_utc(datetime.now(timezone('Europe/Stockholm')))
    >>> d.tzinfo == utc
    True

    :param date: the datetime object to be checked.
    :return: datetime instance of the same time but ensured to be utc timezone.
    """
    if date.tzinfo is None or date.tzinfo.utcoffset(date) is None:
        date = utc.localize(date)
    return date
