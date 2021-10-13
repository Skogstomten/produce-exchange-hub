from datetime import datetime

from firebase_admin.firestore import client as get_firestore_client
from flask import g, Flask
from google.cloud.firestore_v1 import Client, DocumentSnapshot

from app import get_firebase_app
from app.companies_endpoint.company import Company
from app.companies_endpoint.news_feed_post import NewsFeedPost
from app.companies_endpoint.notification import Notification
from app.errors import NotFoundError


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
        company_snapshot = self._db.collection('companies').document(company_id)
        company_languages = company_snapshot.get(('content_languages_iso',)).to_dict().get('content_languages_iso')
        feed = company_snapshot.collection('news_feed').get()
        for post in feed:
            yield NewsFeedPost(post.id, post.to_dict(), user_language, company_languages)

    def get_company_notifications(self, company_id: str, user_language: str) -> list[Notification]:
        company_document_reference = self._db.collection('companies').document(company_id)
        company_snapshot = company_document_reference.get(('content_languages_iso',))
        company_languages = company_snapshot.to_dict().get('content_languages_iso')
        notifications = company_document_reference.collection('notifications').get()
        for notification in notifications:
            yield Notification(notification.id, notification.to_dict(), user_language, company_languages)

    def close_db(self):
        self._db.close()

    def add_company_news_feed_post(self,
                                   company_id: str,
                                   user_id: str,
                                   data: dict[str, dict],
                                   date: datetime) -> str:
        company_doc_ref = self._db.collection('companies').document(company_id)
        company_snapshot = company_doc_ref.get()
        user_doc_ref = self._db.collection('users').document(user_id)

        if not company_snapshot.exists:
            raise NotFoundError(company_id)

        news_feed_collection = company_doc_ref.collection('news_feed')
        post_doc_ref = news_feed_collection.document()

        doc_data = {}
        for language_code in data.keys():
            item = data.get(language_code)
            doc_data[language_code] = {
                'title': item.get('title'),
                'body': item.get('body'),
                'posted_date': date,
                'posted_by': user_doc_ref,
            }
        post_doc_ref.create(doc_data)
        return post_doc_ref.get().id

    def get_news_feed_post(self, company_id: str, post_id: str, user_language: str):
        company_doc_ref = self._db.collection('companies').document(company_id)
        company_snapshot = company_doc_ref.get(('content_languages_iso',))
        company_languages = company_snapshot.to_dict().get('content_languages_iso')

        if not company_snapshot.exists:
            raise NotFoundError(company_id)

        post_snapshot = company_doc_ref.collection('news_feed').document(post_id).get()

        if not post_snapshot.exists:
            raise NotFoundError(post_id)

        return NewsFeedPost(post_id, post_snapshot.to_dict(), user_language, company_languages)


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
