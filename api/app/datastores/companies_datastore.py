from typing import List

from fastapi import Depends
from google.cloud.firestore_v1 import DocumentSnapshot, Client

from .base_datastore import BaseDatastore
from ..dependencies.app_headers import AppHeaders
from ..dependencies.firestore import get_db_client
from ..errors.company_not_found_error import CompanyNotFoundError
from ..models.companies.company_brief_out_model import CompanyBriefOutModel
from ..models.companies.company_out_model import CompanyOutModel


class CompaniesDatastore(BaseDatastore):
    def __init__(self, db: Client):
        super().__init__(db)

    def get_companies(self, headers: AppHeaders) -> List[CompanyBriefOutModel]:
        snapshots: list[DocumentSnapshot] = self.db.collection('companies').get()
        for snapshot in snapshots:
            yield CompanyBriefOutModel.create(snapshot.id, snapshot.to_dict(), headers, self)

    def get_company(self, company_id: str, headers: AppHeaders) -> CompanyOutModel:
        ref = self.db.collection('companies').document(company_id)
        snapshot = ref.get()
        if not snapshot.exists:
            raise CompanyNotFoundError(company_id)

        data = snapshot.to_dict()
        return CompanyOutModel.create(company_id, data, headers, self)


async def get_companies_datastore(db: Client = Depends(get_db_client)):
    return CompaniesDatastore(db)
