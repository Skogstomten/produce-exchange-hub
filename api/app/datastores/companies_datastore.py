from typing import List, Dict

from fastapi import Depends
from google.cloud.firestore_v1 import DocumentSnapshot, Client

from .base_datastore import BaseDatastore
from ..dependencies.firestore import get_db_client
from ..models.companies.company_api_list_model import CompanyApiListModel


class CompaniesDatastore(BaseDatastore):
    def __init__(self, db: Client):
        super().__init__(db)

    def get_companies(self, language: str) -> List[Dict]:
        snapshots: list[DocumentSnapshot] = self.db.collection('companies').get()
        for snapshot in snapshots:
            yield CompanyApiListModel.create(snapshot.id, snapshot.to_dict(), language, self)


async def get_companies_datastore(db: Client = Depends(get_db_client)):
    return CompaniesDatastore(db)
