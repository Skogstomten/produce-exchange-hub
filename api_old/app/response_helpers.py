from flask import make_response, jsonify, Response
from jsonschema import ValidationError

from app.errors import NotFoundError


def not_found_response(err: NotFoundError) -> Response:
    message = {
        'error': err.message,
        'status': 404,
    }
    return make_response(jsonify(message), 404)


def updated_response(data: dict) -> Response:
    return make_response(jsonify(data), 202)


def validation_error_response(err: ValidationError):
    message = {
        'status': 400,
        'message': err.message,
    }
    return make_response(jsonify(message), 400)
