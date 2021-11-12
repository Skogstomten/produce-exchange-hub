from typing import List

from fastapi import Depends
from azure.cosmos import DatabaseProxy

from .base_datastore import BaseDatastore
from ..dependencies.app_headers import AppHeaders
from ..dependencies.cosmos_db import get_database_proxy
from ..models.companies.company_in_model import CompanyInModel
from ..models.companies.company_out_model import CompanyOutModel
from ..models.companies.company_status import CompanyStatus


class CompaniesDatastore(BaseDatastore[CompanyOutModel]):
    def __init__(self, db: DatabaseProxy):
        super().__init__(db, 'companies')

    def get_companies(self, headers: AppHeaders) -> List[CompanyOutModel]:
        for item in self.container.query_items(
            query='select * from companies',
            enable_cross_partition_query=True,
        ):
            yield CompanyOutModel.create(item.get('id'), item, headers, self)

    def get_company(self, company_id: str, headers: AppHeaders) -> CompanyOutModel:
        pass
        # return self.get(company_id, lambda doc_id, data: CompanyOutModel.create(doc_id, data, headers, self))

    def add_company(self, body: CompanyInModel, headers: AppHeaders) -> CompanyOutModel:
        document = self.container.upsert_item(body.to_database_dict(CompanyStatus.unactivated))
        return CompanyOutModel.create(document.get('id'), document, headers, self)

    def update_company(self, company_id: str, body: CompanyInModel, headers: AppHeaders) -> CompanyOutModel:
        # ref, snapshot = self._get_ref_and_snapshot(company_id, ('status',))
        # status: CompanyStatus = snapshot.to_dict().get('status')
        # ref.set(body.to_database_dict(status))
        return self.get_company(company_id, headers)

    def delete_company(self, company_id: str):
        self.delete(company_id)


async def get_companies_datastore(db: DatabaseProxy = Depends(get_database_proxy)):
    return CompaniesDatastore(db)
