from abc import ABC
from collections.abc import Iterable


class StringValues(Iterable[str], ABC):
    def __init__(self, *args):
        self.values = []
        for arg in args:
            self.values.append(str(arg))

    def append(self, *args):
        for arg in args:
            self.values.append(str(arg))

    def __iter__(self):
        return self.values.__iter__()


class QueryParameter:
    def __init__(self, param_name: str, value: StringValues):
        self.param_name = param_name
        if value is None:
            self.values = StringValues()
        else:
            self.values = value

    def __str__(self):
        val = self.param_name
        for str_val in self.values:
            if val == self.param_name:
                val += f"={str_val}"
            else:
                val += f"&{self.param_name}={str_val}"
        return val


class QueryStringParser(Iterable[QueryParameter], ABC):
    def __init__(self, query_string: str):
        self._query_string_raw = query_string

        query_parameters = query_string.split('&')
        self.query_parameters: dict[str, QueryParameter] = {}
        for query_parameter in query_parameters:
            parts = query_parameter.split('=')
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
