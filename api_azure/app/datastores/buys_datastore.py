from typing import List, NoReturn

from fastapi import Depends
from azure.cosmos import DatabaseProxy

from .base_datastore import BaseDatastore
from ..dependencies.app_headers import AppHeaders
from ..dependencies.cosmos_db import get_database_proxy
from ..models.companies.buys.buys_in_model import BuysInModel
from ..models.companies.buys.buys_out_model import BuysOutModel


class BuysDatastore(BaseDatastore[BuysOutModel]):
    def __init__(self, db: DatabaseProxy):
        super(BuysDatastore, self).__init__(db, 'companies')

    def get_buys(self, company_id: str, headers: AppHeaders) -> List[BuysOutModel]:
        # company_ref, company_snapshot = self._get_ref_and_snapshot(company_id, ('content_languages_iso',))
        # languages = company_snapshot.to_dict().get('content_languages_iso')
        # snapshots = company_ref.collection('buys').get()
        # for snapshot in snapshots:
        #     yield BuysOutModel.create(snapshot.id, snapshot.to_dict(), headers, languages, self)
        return []

    def get_buys_post(self, company_id: str, buys_id: str, headers: AppHeaders) -> BuysOutModel:
        # company_ref, company_snapshot = self._get_ref_and_snapshot(company_id, ('content_languages_iso',))
        # ref, snapshot = self._get_ref_and_snapshot(buys_id, parent_doc_ref=company_ref, sub_collection_name='buys')
        # languages = company_snapshot.to_dict().get('content_languages_iso')
        # return BuysOutModel.create(buys_id, snapshot.to_dict(), headers, languages, self)
        pass

    def add_buys_post(self, company_id: str, body: BuysInModel, headers: AppHeaders) -> BuysOutModel:
        # company_ref, company_snapshot = self._get_ref_and_snapshot(company_id)
        # ref = company_ref.collection('buys').document()
        # ref.create(body.to_database_dict())
        # return self.get_buys_post(company_id, ref.id, headers)
        pass

    def update_buys_post(self, company_id: str, buys_id: str, body: BuysInModel, headers: AppHeaders) -> BuysOutModel:
        # company_ref, company_snapshot = self._get_ref_and_snapshot(company_id)
        # ref, snapshot = self._get_ref_and_snapshot(buys_id, parent_doc_ref=company_ref, sub_collection_name='buys')
        # ref.set(body.to_database_dict())
        # return self.get_buys_post(company_id, buys_id, headers)
        pass

    def delete_buys(self, company_id: str, buys_id: str) -> NoReturn:
        # self._get_ref_and_snapshot(
        #     buys_id,
        #     parent_doc_ref=self._get_ref_and_snapshot(company_id)[0],
        #     sub_collection_name='buys'
        # )[0].delete()
        pass


def get_buys_datastore(client: DatabaseProxy = Depends(get_database_proxy)) -> BuysDatastore:
    return BuysDatastore(client)
