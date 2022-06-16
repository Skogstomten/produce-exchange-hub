"""
Module containing utility methods related to enums.
"""
from enum import Enum
from collections.abc import MutableMapping


def enums_to_string(data: MutableMapping) -> MutableMapping:
    """
    Traverses a MutableMapping and checks if it contains any enums, and if so, converts them to str.

    :param data: The mapping to check
    :return: mapping with all enum values converted to string values.
    """
    for key, value in data.items():
        if isinstance(value, Enum):
            data[key] = value.value
        if isinstance(value, list):
            for index, item in enumerate(value):
                if isinstance(item, Enum):
                    value[index] = item.value
    return data
