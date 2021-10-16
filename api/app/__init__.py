import os
import traceback

from flask import Flask, jsonify, make_response

from firebase_admin.credentials import Certificate
from firebase_admin import App, initialize_app as init_firebase
from jsonschema import ValidationError
from werkzeug.exceptions import NotFound

from app.errors import NotFoundError
from app.response_helpers import not_found_response, validation_error_response

_credentials = Certificate('./produce-exchange-hub-firebase-adminsdk-ufzci-78e6592558.json')
_options = {"databaseURL": "https://produce-exchange-hub.firebaseio.com"}
_firebase_app: App = init_firebase(_credentials, _options, __name__)


def get_firebase_app() -> App:
    return _firebase_app


def create_app(test_config=None) -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'app.sqlite'),
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)

    # Make sure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from .database_access import firestore

    @app.route('/ping')
    def ping() -> str:
        return "I was pinged and responded!"

    @app.errorhandler(Exception)
    def handle_error(e):
        if isinstance(e, NotFoundError):
            return not_found_response(e)

        if isinstance(e, ValidationError):
            return validation_error_response(e)

        if isinstance(e, NotFound):
            return make_response(jsonify({
                'status': 404,
                'message': e.description,
            }), 404)

        return make_response(jsonify({
            'status': 500,
            'error': str(e),
            'trace': traceback.format_exc()
        }), 500)

    app.register_error_handler(Exception, handle_error)

    from . import users
    app.register_blueprint(users.bp)

    from app.companies_endpoint import companies
    app.register_blueprint(companies.bp)

    from app.companies_endpoint import company_news_feed
    app.register_blueprint(company_news_feed.bp)

    from app.companies_endpoint import company_notifications
    app.register_blueprint(company_notifications.bp)

    return app
