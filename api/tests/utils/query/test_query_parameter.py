from unittest import TestCase

from app.utils.query.query_parameter import QueryParameter
from app.utils.string_values import StringValues


class QueryParameterTest(TestCase):
    def test_can_initialize(self):
        target = QueryParameter('test', StringValues('val'))
        self.assertEqual(target.param_name, 'test')
        self.assertEqual(target.values.values[0], 'val')

    def test_can_initialize_with_only_one_value(self):
        target = QueryParameter('name', 123, 345)
        self.assertEqual(target.values.values[0], '123')
        self.assertEqual(target.values.values[0], '345')

    def test_str(self):
        target = QueryParameter('name')
        self.assertEqual(str(target), 'name')
        target = QueryParameter('name', 'val')
        self.assertEqual(str(target), 'name=val')
        target = QueryParameter('name', 'val1', 'val2')
        self.assertEqual(str(target), 'name=val1&name=val2')
    