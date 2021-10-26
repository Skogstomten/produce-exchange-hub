from typing import List

from fastapi import Depends
from google.cloud.firestore_v1 import Client, DocumentSnapshot, DocumentReference

from app.datastores.companies_datastore import CompaniesDatastore
from app.dependencies.app_headers import AppHeaders
from app.dependencies.firestore import get_db_client
from app.errors.not_found_error import NotFoundError
from app.models.companies.news_feed.news_feed_brief_out_model import NewsFeedBriefOutModel
from app.models.companies.news_feed.news_feed_full_out_model import NewsFeedFullOutModel
from app.models.companies.news_feed.news_feed_post_put_model import NewsFeedPostPutModel


def _get_post_ref_and_snapshot(
        company_ref: DocumentReference,
        post_id: str
) -> tuple[DocumentReference, DocumentSnapshot]:
    ref = company_ref.collection('news_feed').document(post_id)
    snapshot = ref.get()
    if not snapshot.exists:
        raise NotFoundError(f"News feed post with id '{post_id}' was not found")
    return ref, snapshot


class NewsFeedDatastore(CompaniesDatastore):
    def __init__(self, db: Client):
        super(NewsFeedDatastore, self).__init__(db)

    def get_news_feed(self, company_id: str, headers: AppHeaders) -> List[NewsFeedBriefOutModel]:
        company_ref, company_snapshot = self._get_company_ref_and_snapshot(company_id)
        company_languages = company_snapshot.to_dict().get('content_languages_iso')
        news_feed_snapshots: list[DocumentSnapshot] = company_ref.collection('news_feed').get()
        for snapshot in news_feed_snapshots:
            yield NewsFeedBriefOutModel.create(snapshot.id, snapshot.to_dict(), headers, company_languages, self)

    def get_news_feed_post(self, company_id: str, post_id: str, headers: AppHeaders) -> NewsFeedFullOutModel:
        company_ref, company_snapshot = self._get_company_ref_and_snapshot(company_id)
        post_ref, post_snapshot = _get_post_ref_and_snapshot(company_ref, post_id)
        return NewsFeedFullOutModel.create(post_id, post_snapshot.to_dict(), headers)

    def add_news_feed_post(
            self,
            company_id: str,
            headers: AppHeaders,
            body: NewsFeedPostPutModel
    ) -> NewsFeedFullOutModel:
        company_ref, company_snapshot = self._get_company_ref_and_snapshot(company_id)
        post_ref: DocumentReference = company_ref.collection('news_feed').document()
        post_ref.create(body.to_database_dict(self))
        return self.get_news_feed_post(company_id, post_ref.id, headers)

    def update_news_feed_post(
            self,
            company_id: str,
            post_id: str,
            body: NewsFeedPostPutModel,
            headers: AppHeaders
    ) -> NewsFeedFullOutModel:
        company_ref, company_snapshot = self._get_company_ref_and_snapshot(company_id)
        post_ref, post_snapshot = _get_post_ref_and_snapshot(company_ref, post_id)
        post_ref.set(body.to_database_dict(self))
        return self.get_news_feed_post(company_id, post_ref.id, headers)

    def delete_news_feed_post(self, company_id: str, post_id: str):
        company_ref, company_snapshot = self._get_company_ref_and_snapshot(company_id)
        post_ref, post_snapshot = _get_post_ref_and_snapshot(company_ref, post_id)
        post_ref.delete()


def get_news_feed_datastore(
        db_client: Client = Depends(get_db_client)
) -> NewsFeedDatastore:
    return NewsFeedDatastore(db_client)
