from firebase_admin.firestore import client as get_firestore_client
from flask import g, Flask
from google.cloud.firestore_v1 import Client, DocumentSnapshot

from app.errors import NotFoundError
from app import get_firebase_app
from app.company import Company
from app.news_feed_post import NewsFeedPost


class DocumentDatabase(object):
    def __init__(self, db: Client):
        self._db = db

    def list_users(self) -> list[DocumentSnapshot]:
        return self._db.collection('users').get()

    def list_companies(self) -> list[DocumentSnapshot]:
        return self._db.collection('companies').get()

    def get_company(self, company_id: str) -> Company:
        document_snapshot = self._db.collection('companies').document(company_id).get()
        if document_snapshot.exists:
            data = document_snapshot.to_dict()
            return Company(document_snapshot.id, data)
        raise NotFoundError(company_id)

    def get_localization(self, document_key: str) -> dict[str, str]:
        document_snapshot = self._db.collection('localization').document(document_key).get()
        if document_snapshot.exists:
            return document_snapshot.to_dict()
        return {}

    def get_news_feed(self, company_id: str, user_language: str) -> list[NewsFeedPost]:
        feed = self._db.collection('companies').document(company_id).collection('news_feed').get()
        for post in feed:
            yield NewsFeedPost(post.id, post.to_dict(), user_language)

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
