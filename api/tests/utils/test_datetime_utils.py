from datetime import datetime
from pytz import utc

from app.utils.datetime_utils import ensure_utc


def test_ensure_utc_naive_datetime_gets_converted():
    naive_datetime = datetime.now()

    utc_datetime = ensure_utc(naive_datetime)

    assert utc_datetime is not None
    assert utc_datetime.tzinfo is not None
    assert utc_datetime.tzinfo == utc


def test_ensure_utc_utc_datetime_remains_the_same():
    utc_datetime = datetime.now(utc)

    utc_datetime = ensure_utc(utc_datetime)

    assert utc_datetime.tzinfo is not None
    assert utc_datetime.tzinfo == utc
