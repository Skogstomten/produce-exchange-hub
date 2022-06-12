from unittest import TestCase

from app.utils.string_values import StringValues


class StringValuesTest(TestCase):
    def test_can_create_string_values_without_values(self):
        target = StringValues()
        self.assertIsNotNone(target.values)
        self.assertEqual(len(target.values), 0)

    def test_can_create_with_values_and_values_are_correct(self):
        target = StringValues('val1', 'val2', 'val3')
        self.assertListEqual(target.values, ['val1', 'val2', 'val3'])

    def test_can_append_values(self):
        target = StringValues('val1')
        self.assertListEqual(target.values, ['val1'])
        target.append('val2', 'val3')
        self.assertListEqual(target.values, ['val1', 'val2', 'val3'])

    def test_can_iterate(self):
        target = StringValues('val1', 'val2')
        for index, val in enumerate(target):
            if index == 0:
                self.assertEqual(val, 'val1')
            elif index == 1:
                self.assertEqual(val, 'val2')
            else:
                self.fail(f"Index {index} is not supposed to be a thing...")

    def test_can_get_size_of(self):
        target = StringValues('1', '2')
        self.assertEqual(len(target), 2)
