from typing import List

from fastapi import Depends
from google.cloud.firestore_v1 import Client

from .base_datastore import BaseDatastore
from ..dependencies.app_headers import AppHeaders
from ..dependencies.firestore import get_db_client
from ..models.companies.company_in_model import CompanyInModel
from ..models.companies.company_out_model import CompanyOutModel
from ..models.companies.company_status import CompanyStatus


class CompaniesDatastore(BaseDatastore[CompanyOutModel]):
    def __init__(self, db: Client):
        super().__init__(db, 'companies')

    def get_companies(self, headers: AppHeaders) -> List[CompanyOutModel]:
        return self.get_all(lambda snapshot: CompanyOutModel.create(snapshot.id, snapshot.to_dict(), headers, self))

    def get_company(self, company_id: str, headers: AppHeaders) -> CompanyOutModel:
        return self.get(company_id, lambda doc_id, data: CompanyOutModel.create(doc_id, data, headers, self))

    def add_company(self, body: CompanyInModel, headers: AppHeaders) -> CompanyOutModel:
        return self.add(
            lambda: body.to_database_dict(CompanyStatus.unactivated),
            lambda doc_id, data: CompanyOutModel.create(doc_id, data, headers, self)
        )

    def update_company(self, company_id: str, body: CompanyInModel, headers: AppHeaders) -> CompanyOutModel:
        ref, snapshot = self._get_ref_and_snapshot(company_id, ('status',))
        status: CompanyStatus = snapshot.to_dict().get('status')
        ref.set(body.to_database_dict(status))
        return self.get_company(company_id, headers)

    def delete_company(self, company_id: str):
        self.delete(company_id)


async def get_companies_datastore(db: Client = Depends(get_db_client)):
    return CompaniesDatastore(db)
