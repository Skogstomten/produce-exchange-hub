from app.utils.string_values import StringValues


class QueryParameter:
    def __init__(self, param_name: str, *args):
        self.param_name = param_name
        self.values = StringValues()
        for arg in args:
            self.values.append(arg)

    def __str__(self):
        val = self.param_name
        for str_val in self.values:
            if val == self.param_name:
                val += f"={str_val}"
            else:
                val += f"&{self.param_name}={str_val}"
        return val
