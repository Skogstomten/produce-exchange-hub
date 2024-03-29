"""Tests for enum_utils."""
from enum import Enum

from app.shared.models.v1.shared import Language
from app.database.mongo.enum_utils import enums_to_string


class TestEnum(Enum):
    """Enum used for test."""

    value1 = "value1"


def test_enums_to_string():
    assert enums_to_string({"value": TestEnum.value1}) == {"value": TestEnum.value1.value}


def test_enums_to_string_with_nested_list():
    assert enums_to_string({"sub_list": [TestEnum.value1]}) == {"sub_list": [TestEnum.value1.value]}


def test_enums_to_string_with_nested_dict():
    assert enums_to_string({"sub_dict": {"val": TestEnum.value1}}) == {"sub_dict": {"val": TestEnum.value1.value}}


def test_enums_to_string_with_list_of_dicts():
    input_dict = {"things": [{"val": TestEnum.value1}]}
    expected_dict = {"things": [{"val": TestEnum.value1.value}]}

    assert enums_to_string(input_dict) == expected_dict


def test_enums_to_strings_converts_enum_keys():
    input_dict = {Language.SV: "Detta är text"}
    expected_dict = {"SV": "Detta är text"}
    assert enums_to_string(input_dict) == expected_dict
