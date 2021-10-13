from flask import make_response, jsonify, Response

from app.errors import NotFoundError


def not_found_response(err: NotFoundError) -> Response:
    message = {
        'error': err.message,
        'status': 404,
    }
    return make_response(jsonify(message), 404)
