from typing import List
from datetime import datetime
import pytz
from warnings import filters

from fastapi import Depends

from .base_datastore import BaseDatastore
from ..dependencies.app_headers import AppHeaders
from ..dependencies.document_database import get_document_database
from ..models.companies.company_in_model import CompanyInModel
from ..models.companies.company_out_model import CompanyOutModel
from ..models.companies.company_status import CompanyStatus
from ..database.document_database import DocumentDatabase
from ..models.shared.sort_order import SortOrder


class CompaniesDatastore(BaseDatastore[CompanyOutModel]):
    def __init__(self, db: DocumentDatabase):
        super().__init__(db)

    def get_companies(
        self,
        headers: AppHeaders,
        take: int | None,
        sort_by: str | None,
        sort_order: SortOrder,
        active_only: bool,
    ) -> List[CompanyOutModel]:
        filters = None
        if active_only:
            filters = {'status': CompanyStatus.active.value}
        return self.db.collection(
            'companies'
        ).get(
            filters
        ).take(
            take
        ).sort(
            sort_by, sort_order
        ).select_for_each(
            lambda doc: CompanyOutModel.create(doc.id, doc, headers, self)
        )

    def get_company(self, company_id: str, headers: AppHeaders) -> CompanyOutModel:
        return self.db.collection('companies').by_id(company_id).to(
            lambda doc: CompanyOutModel.create(doc.id, doc, headers, self)
        )

    def add_company(self, body: CompanyInModel, headers: AppHeaders) -> CompanyOutModel:
        return self.db.collection('companies').add(
            body.to_database_dict(CompanyStatus.unactivated.value)
        ).to(lambda doc: CompanyOutModel.create(doc.id, doc, headers, self))

    def activate_company(self, company_id: str, headers: AppHeaders) -> CompanyOutModel:
        company = self.db.collection('companies').by_id(company_id)
        company['status'] = CompanyStatus.active.value
        company['activation_date'] = datetime.now(pytz.utc)
        company.update()
        return self.get_company(company_id, headers)

    # def update_company(self, company_id: str, body: CompanyInModel, headers: AppHeaders) -> CompanyOutModel:
    #     ref, snapshot = self._get_ref_and_snapshot(company_id, ('status',))
    #     status: CompanyStatus = snapshot.to_dict().get('status')
    #     ref.set(body.to_database_dict(status))
    #     return self.get_company(company_id, headers)
    #
    # def delete_company(self, company_id: str):
    #     self.delete(company_id)


async def get_companies_datastore(db: DocumentDatabase = Depends(get_document_database)):
    return CompaniesDatastore(db)
