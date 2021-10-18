from datetime import datetime

import pytz

from .companies_datastore import CompaniesDatastore
from .news_feed_post import NewsFeedPost

from app.errors import NotFoundError
from app.datetime_helpers import format_date


class NewsFeedDatastore(CompaniesDatastore):
    def __init__(self):
        super(NewsFeedDatastore, self).__init__()

    def list_news_feed(self, company_id: str, user_language: str) -> list[NewsFeedPost]:
        company_ref = self.db.collection('companies').document(company_id)
        company_languages = company_ref.get(('content_languages_iso',)).to_dict().get('content_languages_iso')
        feed = company_ref.collection('news_feed').get()
        for post in feed:
            yield NewsFeedPost(post.id, post.to_dict(), user_language, company_languages)

    def add_news_feed_post(self,
                           company_id: str,
                           user_id: str,
                           data: list[dict[str, str]],
                           date: datetime) -> str:
        company_snapshot = self.db.collection('companies').document(company_id).get()
        user_doc_ref = self.db.collection('users').document(user_id)

        if not company_snapshot.exists:
            raise NotFoundError(company_id)

        news_feed_collection = company_snapshot.reference.collection('news_feed')
        post_doc_ref = news_feed_collection.document()

        doc_data = {
            'posted_by': user_doc_ref,
            'posted_date': date,
            'post': {},
        }
        for item in data:
            doc_data['post'][item.get('language_iso')] = {
                'title': item.get('title'),
                'body': item.get('body'),
            }
        post_doc_ref.create(doc_data)
        return post_doc_ref.get().id

    def get_news_feed_post(self, company_id: str, post_id: str, user_language: str):
        company_doc_ref = self.db.collection('companies').document(company_id)
        company_snapshot = company_doc_ref.get(('content_languages_iso',))
        company_languages = company_snapshot.to_dict().get('content_languages_iso')

        if not company_snapshot.exists:
            raise NotFoundError(company_id)

        post_snapshot = company_doc_ref.collection('news_feed').document(post_id).get()

        if not post_snapshot.exists:
            raise NotFoundError(post_id)

        return NewsFeedPost(post_id, post_snapshot.to_dict(), user_language, company_languages)

    def delete_news_feed_post(self, company_id: str, post_id: str):
        company_doc_ref = self.db.collection('companies').document(company_id)
        company_snapshot = company_doc_ref.get()
        if not company_snapshot.exists:
            raise NotFoundError(company_id)

        company_doc_ref.collection('news_feed').document(post_id).delete()

    def update_post(self,
                    company_id: str,
                    post_id: str,
                    user_id: str,
                    post: list[dict[str, str]],
                    user_language: str) -> NewsFeedPost:
        company_snapshot = self.db.collection('companies').document(company_id).get()
        if not company_snapshot.exists:
            raise NotFoundError(company_id)

        post_snapshot = company_snapshot.reference.collection('news_feed').document(post_id).get()
        post_data = post_snapshot.to_dict()
        if not post_snapshot.exists:
            raise NotFoundError(post_id)

        user_ref = self.db.collection('users').document(user_id)

        new_data = {
            'posted_by': post_data.get('posted_by'),
            'posted_date': post_data.get('posted_date'),
            'updated_by': user_ref,
            'updated_date': datetime.now(pytz.timezone('UTC')),
            'post': {},
        }
        for item in post:
            new_data['post'][item.get('language_iso')] = {
                'title': item.get('title'),
                'body': item.get('body'),
            }

        post_snapshot.reference.set(new_data)

        company_languages = company_snapshot.to_dict().get('content_languages_iso')

        return NewsFeedPost(post_snapshot.reference.id, new_data, user_language, company_languages)

    def get_news_feed_raw(self, company_id: str) -> list[dict[str, str]]:
        posts = self.db.collection('companies').document(company_id).collection('news_feed').get()
        for post in posts:
            data = post.to_dict()
            posted_by_snapshot = data.get('posted_by').get()
            posted_by_data = posted_by_snapshot.to_dict()
            result = {
                'posted_by_email': posted_by_snapshot.reference.id,
                'posted_by_name': f"{posted_by_data.get('first_name')} {posted_by_data.get('last_name')}",
                'id': post.reference.id,
                'posted_date': format_date(data.get('posted_date'), 'Europe/Stockholm'),
                'post': data.get('post'),
            }

            if 'updated_by' in data:
                updated_by_snapshot = data.get('updated_by').get()
                updated_by_data = updated_by_snapshot.to_dict()
                result['updated_by_email'] = updated_by_snapshot.reference.id
                result['updated_by_name'] = '{} {}'.format(updated_by_data.get('first_name'),
                                                           updated_by_data.get('last_name'))
            if 'updated_date' in data:
                updated_date = data.get('updated_date')
                result['updated_date'] = format_date(updated_date, 'Europe/Stockholm')

            yield result
