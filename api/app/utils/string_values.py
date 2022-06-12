from abc import ABC
from typing import Iterable, Sized


class StringValues(Iterable[str], Sized, ABC):
    def __init__(self, *args: str):
        self.values = []
        for arg in args:
            self.values.append(str(arg))

    def append(self, *args: str):
        for arg in args:
            self.values.append(str(arg))

    def __iter__(self):
        return self.values.__iter__()

    def __sizeof__(self):
        return len(self.values)

    def __len__(self):
        return len(self.values)
