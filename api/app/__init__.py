import os
from flask import Flask

from firebase_admin.credentials import Certificate
from firebase_admin import App, initialize_app as init_firebase

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

    from . import users
    app.register_blueprint(users.bp)

    from app.companies_endpoint import companies
    app.register_blueprint(companies.bp)

    from app.companies_endpoint import company_news_feed
    app.register_blueprint(company_news_feed.bp)

    from app.companies_endpoint import company_notifications
    app.register_blueprint(company_notifications.bp)

    return app
