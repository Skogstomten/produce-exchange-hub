from firebase_admin.firestore import client as get_firestore_client

from google.cloud.firestore_v1 import Client

from flask import g, Flask

from . import get_firebase_app


class DocumentDatabase(object):
    def __init__(self, db: Client):
        self._db = db

    def list_users(self):
        return self._db.collection('users').get()

    def close_db(self):
        self._db.close()


def get_db() -> DocumentDatabase:
    if 'db' not in g:
        db: Client = get_firestore_client(get_firebase_app())
        g.db = DocumentDatabase(db)

    return g.db


def close_db():
    db: DocumentDatabase = g.pop('db', None)

    if db is not None:
        db.close_db()


def init_app(app: Flask):
    app.teardown_appcontext(close_db)
