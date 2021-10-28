from typing import List, NoReturn

from fastapi import Depends
from google.cloud.firestore_v1 import Client

from .base_datastore import BaseDatastore
from ..models.companies.buys.buys_out_model import BuysOutModel
from ..dependencies.firestore import get_db_client
from ..dependencies.app_headers import AppHeaders


class BuysDatastore(BaseDatastore[BuysOutModel]):
    def __init__(self, db: Client):
        super(BuysDatastore, self).__init__(db, 'companies')

    def get_buys(self, company_id: str, headers: AppHeaders) -> List[BuysOutModel]:
        company_ref, company_snapshot = self._get_ref_and_snapshot(company_id, ('content_languages_iso',))
        languages = company_snapshot.to_dict().get('content_languages_iso')
        snapshots = company_ref.collection('buys').get()
        for snapshot in snapshots:
            yield BuysOutModel.create(snapshot.id, snapshot.to_dict(), headers, languages, self)

    def get_buys_post(self) -> BuysOutModel:
        pass

    def add_buys_post(self) -> BuysOutModel:
        pass

    def update_buys_post(self) -> BuysOutModel:
        pass

    def delete_buys(self) -> NoReturn:
        pass


def get_buys_datastore(client: Client = Depends(get_db_client)) -> BuysDatastore:
    return BuysDatastore(client)
