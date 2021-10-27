from typing import List, Iterable, Dict

from fastapi import Depends
from google.cloud.firestore_v1 import DocumentSnapshot, Client, DocumentReference

from .base_datastore import BaseDatastore
from ..dependencies.app_headers import AppHeaders
from ..dependencies.firestore import get_db_client
from ..errors.company_not_found_error import CompanyNotFoundError
from ..models.companies.company_in_model import CompanyInModel
from ..models.companies.company_out_model import CompanyOutModel
from ..models.companies.company_status import CompanyStatus


class CompaniesDatastore(BaseDatastore):
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

    def _get_company_ref_and_snapshot(
            self,
            company_id: str,
            field_paths: Iterable[str] | None = None
    ) -> tuple[DocumentReference, DocumentSnapshot]:
        ref = self.db.collection('companies').document(company_id)
        snapshot = ref.get(field_paths)
        if not snapshot.exists:
            raise CompanyNotFoundError(company_id)

        return ref, snapshot


async def get_companies_datastore(db: Client = Depends(get_db_client)):
    return CompaniesDatastore(db)
