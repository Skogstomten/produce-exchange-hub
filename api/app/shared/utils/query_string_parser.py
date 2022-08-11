"""
Contains the QueryStringParser class which parses a query string, obviously.
"""
from abc import ABC
from collections.abc import Iterable

from app.shared.utils.string_values import StringValues
from .query_parameter import QueryParameter


class QueryStringParser(Iterable[QueryParameter], ABC):
    """
    Used to parse and handle query string.
    """

    def __init__(self, query_string: str | None):
        """
        Creates a QueryStringParser.
        :param query_string: the query string to be parsed.
        """
        self._query_string_raw = query_string

        if query_string:
            query_parameters = query_string.split("&")
        else:
            query_parameters = []
        self.query_parameters: dict[str, QueryParameter] = {}
        for query_parameter in query_parameters:
            parts = query_parameter.split("=")
            key = None
            value = None
            if len(parts) > 0:
                key = parts[0]
                if len(parts) > 1:
                    value = parts[1]
            if key is not None:
                if key in self.query_parameters:
                    str_values = self.query_parameters.get(key).values
                    if value is not None:
                        str_values.append(value)
                else:
                    if value is None:
                        str_values = StringValues()
                    else:
                        str_values = StringValues(value)
                    self.query_parameters.update({key: QueryParameter(key, str_values)})

    def __iter__(self):
        """
        Iterating the query string parser will iterate over
        the individual query parameters found in the query string
        :return:
        """
        return self.query_parameters.values().__iter__()

    def remove(self, parameter_name: str) -> "QueryStringParser":
        """
        Removes a query parameter from the current query string parameter
        :param parameter_name:
        :return:
        """
        if parameter_name in self.query_parameters:
            del self.query_parameters[parameter_name]
        return self
