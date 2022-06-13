from enum import Enum

from app.utils.enum_utils import enums_to_string


class TestEnum(Enum):
    value1 = 'value1'


def test_enums_to_string():
    input_dict = {'value': TestEnum.value1}

    result = enums_to_string(input_dict)

    assert result == {'value': TestEnum.value1.value}
