from enum import Enum


def enums_to_string(data: dict) -> dict:
    for key, value in data.items():
        if isinstance(value, Enum):
            data[key] = value.value
        if isinstance(value, list):
            for index, item in enumerate(value):
                if isinstance(item, Enum):
                    value[index] = item.value
    return data
