"""
Module containing utility methods related to enums.
"""
from enum import Enum
from typing import Any


def enums_to_string(data: Any) -> Any:
    """
    Traverses a MutableMapping and checks if it contains any enums, and if so,
    converts them to str.

    :param data: The mapping to check
    :return: mapping with all enum values converted to string values.
    """
    if isinstance(data, dict):
        data_clone = data.copy()
        for key, value in data_clone.items():
            if isinstance(key, Enum):
                new_key = key.value
                del data[key]
                data[new_key] = value
                key = new_key
            data[key] = enums_to_string(value)
    elif isinstance(data, list):
        for index, value in enumerate(data):
            data[index] = enums_to_string(value)
    elif isinstance(data, Enum):
        data = data.value

    return data
