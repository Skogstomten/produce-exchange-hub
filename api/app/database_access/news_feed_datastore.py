from datetime import datetime

from .companies_datastore import CompaniesDatastore
from .news_feed_post import NewsFeedPost

from app.errors import NotFoundError


class NewsFeedDatastore(CompaniesDatastore):
    def __init__(self):
        super(NewsFeedDatastore, self).__init__()

    def list_news_feed(self, company_id: str, user_language: str) -> list[NewsFeedPost]:
        company_snapshot = self.db.collection('companies').document(company_id)
        company_languages = company_snapshot.get(('content_languages_iso',)).to_dict().get('content_languages_iso')
        feed = company_snapshot.collection('news_feed').get()
        for post in feed:
            yield NewsFeedPost(post.id, post.to_dict(), user_language, company_languages)

    def add_news_feed_post(self,
                           company_id: str,
                           user_id: str,
                           data: dict[str, dict],
                           date: datetime) -> str:
        company_doc_ref = self.db.collection('companies').document(company_id)
        company_snapshot = company_doc_ref.get()
        user_doc_ref = self.db.collection('users').document(user_id)

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
