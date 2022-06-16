"""
Module for the QueryParameter class
"""
from app.utils.string_values import StringValues


class QueryParameter:
    """
    Represents a single query parameter
    """
    def __init__(self, param_name: str, *args) -> None:
        """
        Creates a query parameter with name and one or more values that will be stringified

        >>> str(QueryParameter('name'))
        name

        >>> str(QueryParameter('name', 'val'))
        name=val

        >>> str(QueryParameter('name', 'val1', 'val2'))
        name=val1&name=val2

        :param param_name: name of query parameter
        :param args: query parameter values
        """
        self.param_name = param_name
        self.values = StringValues()
        for arg in args:
            self.values.append(arg)

    def __str__(self) -> str:
        """
        Converts instance to url format.
        :return:
        """
        val = self.param_name
        for str_val in self.values:
            if val == self.param_name:
                val += f"={str_val}"
            else:
                val += f"&{self.param_name}={str_val}"
        return val
