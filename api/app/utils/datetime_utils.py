from datetime import datetime
import pytz


def ensure_utc(d: datetime):
    if d.tzinfo is None or d.tzinfo.utcoffset(d) is None:
        d = pytz.utc.localize(d)
    return d
