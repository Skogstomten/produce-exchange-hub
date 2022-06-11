from enum import Enum
from unittest import TestCase

from app.utils.enum_utils import enums_to_string


class TestEnum(Enum):
    value1 = 'value1'


class EnumUtilsTest(TestCase):
    def test_enums_to_string(self):
        input_dict = {'value': TestEnum.value1}
        result = enums_to_string(input_dict)
        self.assertDictEqual(result, {'value': TestEnum.value1.value})
