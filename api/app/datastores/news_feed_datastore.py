from fastapi import Depends
from google.cloud.firestore_v1 import Client

from app.datastores.base_datastore import BaseDatastore
from app.dependencies.app_headers import AppHeaders
from app.dependencies.firestore import get_db_client


class NewsFeedDatastore(BaseDatastore):
    def __init__(self, db: Client):
        super(NewsFeedDatastore, self).__init__(db)

    def get_news_feed(self, company_id: str, headers: AppHeaders):
        pass


def get_news_feed_datastore(
        db_client: Client = Depends(get_db_client)
) -> NewsFeedDatastore:
    return NewsFeedDatastore(db_client)
