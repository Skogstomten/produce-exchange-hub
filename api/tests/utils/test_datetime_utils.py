from unittest import TestCase
from datetime import datetime
from pytz import utc

from app.utils.datetime_utils import ensure_utc


class DateTimeUtilsTest(TestCase):
    def test_ensure_utc_naive_datetime_gets_converted(self):
        naive_datetime = datetime.now()
        self.assertIsNone(naive_datetime.tzinfo)
        utc_datetime = ensure_utc(naive_datetime)
        self.assertIsNotNone(utc_datetime)
        self.assertIsNotNone(utc_datetime.tzinfo)
        self.assertEqual(utc_datetime.tzinfo, utc)

    def test_ensure_utc_utc_datetime_remains_the_same(self):
        utc_datetime = datetime.now(utc)
        self.assertIsNotNone(utc_datetime.tzinfo)
        self.assertEqual(utc_datetime.tzinfo, utc)
        utc_datetime = ensure_utc(utc_datetime)
        self.assertIsNotNone(utc_datetime.tzinfo)
        self.assertEqual(utc_datetime.tzinfo, utc)
