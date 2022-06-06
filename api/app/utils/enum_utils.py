from enum import Enum
from collections.abc import MutableMapping


def enums_to_string(data: MutableMapping) -> MutableMapping:
    for key, value in data.items():
        if isinstance(value, Enum):
            data[key] = value.value
        if isinstance(value, list):
            for index, item in enumerate(value):
                if isinstance(item, Enum):
                    value[index] = item.value
    return data
