from flask import g, Flask

from firebase_admin.firestore import client as get_firestore_client
from google.cloud.firestore_v1.client import Client

from app import get_firebase_app


def get_db_client() -> Client:
    if 'firestore_client' not in g:
        client = get_firestore_client(get_firebase_app())
        g.firestore_client = client

    return g.firestore_client


def close_db():
    db: Client = g.pop('firestore_client', None)

    if db is not None:
        db.close()


def init_app(app: Flask):
    app.teardown_appcontext(close_db)
