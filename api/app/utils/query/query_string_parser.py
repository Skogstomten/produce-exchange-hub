from abc import ABC
from collections.abc import Iterable

from app.utils.string_values import StringValues
from .query_parameter import QueryParameter


class QueryStringParser(Iterable[QueryParameter], ABC):
    def __init__(self, query_string: str | None):
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
        return self.query_parameters.values().__iter__()

    def remove(self, parameter_name: str) -> "QueryStringParser":
        if parameter_name in self.query_parameters:
            del self.query_parameters[parameter_name]
        return self
