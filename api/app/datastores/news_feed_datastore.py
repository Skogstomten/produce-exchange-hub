from typing import List

from fastapi import Depends
from google.cloud.firestore_v1 import Client, DocumentSnapshot, DocumentReference

from app.datastores.base_datastore import BaseDatastore
from app.dependencies.app_headers import AppHeaders
from app.dependencies.firestore import get_db_client
from app.errors.company_not_found_error import CompanyNotFoundError
from app.errors.not_found_error import NotFoundError
from app.models.news_feed.news_feed_brief_out_model import NewsFeedBriefOutModel
from app.models.news_feed.news_feed_full_out_model import NewsFeedFullOutModel
from app.models.news_feed.news_feed_post_model import NewsFeedPostModel


class NewsFeedDatastore(BaseDatastore):
    def __init__(self, db: Client):
        super(NewsFeedDatastore, self).__init__(db)

    def get_news_feed(self, company_id: str, headers: AppHeaders) -> List[NewsFeedBriefOutModel]:
        company_ref = self.db.collection('companies').document(company_id)
        company_snapshot = company_ref.get(('content_languages_iso',))
        if not company_snapshot.exists:
            raise CompanyNotFoundError(company_id)

        company_languages = company_snapshot.to_dict().get('content_languages_iso')
        news_feed_snapshots: list[DocumentSnapshot] = company_ref.collection('news_feed').get()
        for snapshot in news_feed_snapshots:
            yield NewsFeedBriefOutModel.create(snapshot.id, snapshot.to_dict(), headers, company_languages, self)

    def get_news_feed_post(self, company_id: str, post_id: str, headers: AppHeaders) -> NewsFeedFullOutModel:
        company_ref = self.db.collection('companies').document(company_id)
        company_snapshot = company_ref.get(('content_languages_iso',))
        if not company_snapshot.exists:
            raise CompanyNotFoundError(company_id)

        post_ref = company_ref.collection('news_feed').document(post_id)
        post_snapshot = post_ref.get()
        if not post_snapshot.exists:
            raise NotFoundError(f"News feed post with id '{post_id}' was not found")

        return NewsFeedFullOutModel.create(post_id, post_snapshot.to_dict(), headers)

    def add_news_feed_post(self, company_id: str, headers: AppHeaders, body: NewsFeedPostModel) -> NewsFeedFullOutModel:
        company_ref = self.db.collection('companies').document(company_id)
        company_snapshot = company_ref.get(('content_languages_iso',))
        if not company_snapshot.exists:
            raise CompanyNotFoundError(company_id)

        post_ref: DocumentReference = company_ref.collection('news_feed').document()
        post_ref.create(body.to_database_dict(self))
        return NewsFeedFullOutModel.create(post_ref.id, post_ref.get().to_dict(), headers)


def get_news_feed_datastore(
        db_client: Client = Depends(get_db_client)
) -> NewsFeedDatastore:
    return NewsFeedDatastore(db_client)
