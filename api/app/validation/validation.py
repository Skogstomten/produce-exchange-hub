import functools

from flask import request
from jsonschema import validate as validate_by_schema


def validate(schema: dict):
    def validate_decorator(function):
        @functools.wraps(function)
        def wrapped_function(**kwargs):
            validate_by_schema(instance=request.json, schema=schema)
            return function(**kwargs)
        return wrapped_function
    return validate_decorator
