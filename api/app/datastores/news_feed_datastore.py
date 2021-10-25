from typing import List

from fastapi import Depends
from google.cloud.firestore_v1 import Client, DocumentSnapshot

from app.datastores.base_datastore import BaseDatastore
from app.dependencies.app_headers import AppHeaders
from app.dependencies.firestore import get_db_client
from app.errors.company_not_found_error import CompanyNotFoundError
from app.models.news_feed.news_feed_out_model import NewsFeedOutModel


class NewsFeedDatastore(BaseDatastore):
    def __init__(self, db: Client):
        super(NewsFeedDatastore, self).__init__(db)

    def get_news_feed(self, company_id: str, headers: AppHeaders) -> List[NewsFeedOutModel]:
        company_ref = self.db.collection('companies').document(company_id)
        company_snapshot = company_ref.get(('content_languages_iso',))
        if not company_snapshot.exists:
            raise CompanyNotFoundError(company_id)

        company_languages = company_snapshot.to_dict().get('content_languages_iso')
        news_feed_snapshots: list[DocumentSnapshot] = company_ref.collection('news_feed').get()
        for snapshot in news_feed_snapshots:
            yield NewsFeedOutModel.create(snapshot.id, snapshot.to_dict(), headers, company_languages, self)


def get_news_feed_datastore(
        db_client: Client = Depends(get_db_client)
) -> NewsFeedDatastore:
    return NewsFeedDatastore(db_client)
