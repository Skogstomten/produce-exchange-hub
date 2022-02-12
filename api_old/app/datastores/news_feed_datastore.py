from typing import List

from fastapi import Depends
from pymongo.database import Database

from ..datastores.base_datastore import BaseDatastore
from ..dependencies.app_headers import AppHeaders
from ..dependencies.user import User
from ..models.companies.news_feed.news_feed_in_model import NewsFeedInModel
from ..models.companies.news_feed.news_feed_out_model import NewsFeedOutModel


class NewsFeedDatastore(BaseDatastore[NewsFeedOutModel]):
    def __init__(self, db: Database):
        super(NewsFeedDatastore, self).__init__(db, 'companies')

#     def get_news_feed(self, company_id: str, headers: AppHeaders) -> List[NewsFeedOutModel]:
#         company_ref, company_snapshot = self._get_ref_and_snapshot(company_id, ('content_languages_iso',))
#         company_languages = company_snapshot.to_dict().get('content_languages_iso')
#         news_feed_snapshots: list[DocumentSnapshot] = company_ref.collection('news_feed').get()
#         for snapshot in news_feed_snapshots:
#             yield NewsFeedOutModel.create(snapshot.id, snapshot.to_dict(), headers, company_languages)
#
#     def get_news_feed_post(self, company_id: str, post_id: str, headers: AppHeaders) -> NewsFeedOutModel:
#         company_ref, company_snapshot = self._get_ref_and_snapshot(company_id, ('content_languages_iso',))
#         post_ref, post_snapshot = self._get_ref_and_snapshot(
#             post_id,
#             parent_doc_ref=company_ref,
#             sub_collection_name='news_feed'
#         )
#         company_languages = company_snapshot.to_dict().get('content_languages_iso')
#         return NewsFeedOutModel.create(post_id, post_snapshot.to_dict(), headers, company_languages)
#
#     def add_news_feed_post(
#             self,
#             company_id: str,
#             headers: AppHeaders,
#             user: User,
#             body: NewsFeedInModel
#     ) -> NewsFeedOutModel:
#         company_ref, company_snapshot = self._get_ref_and_snapshot(company_id)
#         post_ref: DocumentReference = company_ref.collection('news_feed').document()
#         post_ref.create(body.to_database_dict(user, self))
#         return self.get_news_feed_post(company_id, post_ref.id, headers)
#
#     def update_news_feed_post(
#             self,
#             company_id: str,
#             post_id: str,
#             body: NewsFeedInModel,
#             user: User,
#             headers: AppHeaders
#     ) -> NewsFeedOutModel:
#         company_ref, company_snapshot = self._get_ref_and_snapshot(company_id)
#         post_ref, post_snapshot = self._get_ref_and_snapshot(
#             post_id,
#             parent_doc_ref=company_ref,
#             sub_collection_name='news_feed'
#         )
#         post_ref.set(body.to_database_dict(user, self))
#         return self.get_news_feed_post(company_id, post_ref.id, headers)
#
#     def delete_news_feed_post(self, company_id: str, post_id: str):
#         company_ref, company_snapshot = self._get_ref_and_snapshot(company_id)
#         post_ref, post_snapshot = self._get_ref_and_snapshot(
#             post_id,
#             parent_doc_ref=company_ref,
#             sub_collection_name='news_feed'
#         )
#         post_ref.delete()
#
#
# def get_news_feed_datastore(
#         db_client: Client = Depends(get_db_client)
# ) -> NewsFeedDatastore:
#     return NewsFeedDatastore(db_client)
