from typing import List, NoReturn

from fastapi import Depends
from google.cloud.firestore_v1 import Client

from .base_datastore import BaseDatastore
from ..dependencies.app_headers import AppHeaders
from ..dependencies.firestore import get_db_client
from ..models.companies.buys.buys_in_model import BuysInModel
from ..models.companies.buys.buys_out_model import BuysOutModel


class BuysDatastore(BaseDatastore[BuysOutModel]):
    def __init__(self, db: Client):
        super(BuysDatastore, self).__init__(db, 'companies')

    def get_buys(self, company_id: str, headers: AppHeaders) -> List[BuysOutModel]:
        company_ref, company_snapshot = self._get_ref_and_snapshot(company_id, ('content_languages_iso',))
        languages = company_snapshot.to_dict().get('content_languages_iso')
        snapshots = company_ref.collection('buys').get()
        for snapshot in snapshots:
            yield BuysOutModel.create(snapshot.id, snapshot.to_dict(), headers, languages, self)

    def get_buys_post(self, company_id: str, buys_id: str, headers: AppHeaders) -> BuysOutModel:
        company_ref, company_snapshot = self._get_ref_and_snapshot(company_id, ('content_languages_iso',))
        ref, snapshot = self._get_ref_and_snapshot(buys_id, parent_doc_ref=company_ref, sub_collection_name='buys')
        languages = company_snapshot.to_dict().get('content_languages_iso')
        return BuysOutModel.create(buys_id, snapshot.to_dict(), headers, languages, self)

    def add_buys_post(self, company_id: str, body: BuysInModel, headers: AppHeaders) -> BuysOutModel:
        company_ref, company_snapshot = self._get_ref_and_snapshot(company_id)
        ref = company_ref.collection('buys').document()
        ref.create(body.to_database_dict())
        return self.get_buys_post(company_id, ref.id, headers)

    def update_buys_post(self, company_id: str, buys_id: str, body: BuysInModel, headers: AppHeaders) -> BuysOutModel:
        company_ref, company_snapshot = self._get_ref_and_snapshot(company_id)
        ref, snapshot = self._get_ref_and_snapshot(buys_id, parent_doc_ref=company_ref, sub_collection_name='buys')
        ref.set(body.to_database_dict())
        return self.get_buys_post(company_id, buys_id, headers)

    def delete_buys(self, company_id: str, buys_id: str) -> NoReturn:
        self._get_ref_and_snapshot(
            buys_id,
            parent_doc_ref=self._get_ref_and_snapshot(company_id)[0],
            sub_collection_name='buys'
        )[0].delete()


def get_buys_datastore(client: Client = Depends(get_db_client)) -> BuysDatastore:
    return BuysDatastore(client)
