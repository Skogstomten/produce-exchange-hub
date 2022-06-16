"""
Module for the StringValues class
"""
from abc import ABC
from typing import Iterable, Sized


class StringValues(Iterable[str], Sized, ABC):
    """
    Represents one or more string values.
    """

    def __init__(self, *args):
        """
        Creates an instance of StringValues.

        :param args: non str args will be converted to str using the str(arg) function.
        """
        self.values = []
        for arg in args:
            self.values.append(str(arg))

    def append(self, *args) -> None:
        """
        Appends any number of values to the StringValues instance.
        :param args: args of any types. Will be converted to str using the str(arg) function.
        :return: None
        """
        for arg in args:
            if isinstance(arg, StringValues):
                self.values.extend(arg)
            else:
                self.values.append(str(arg))

    def __iter__(self):
        """
        Iterate over all the values in object.
        :return:
        """
        return self.values.__iter__()

    def __len__(self):
        """
        Get the length of the underlying list of values.
        :return:
        """
        return len(self.values)
