from datetime import datetime
from pytz import utc


def ensure_utc(d: datetime):
    if d.tzinfo is None or d.tzinfo.utcoffset(d) is None:
        d = utc.localize(d)
    return d
