from typing import List

from fastapi import Depends
from google.cloud.firestore_v1 import DocumentSnapshot, Client, DocumentReference

from .base_datastore import BaseDatastore
from ..dependencies.app_headers import AppHeaders
from ..dependencies.firestore import get_db_client
from ..errors.company_not_found_error import CompanyNotFoundError
from app.models.companies.out_models.company_brief_out_model import CompanyBriefOutModel
from app.models.companies.out_models.company_out_model import CompanyOutModel
from ..models.companies.in_models.company_post_put_model import CompanyPostPutModel


class CompaniesDatastore(BaseDatastore):
    def __init__(self, db: Client):
        super().__init__(db)

    def get_companies(self, headers: AppHeaders) -> List[CompanyBriefOutModel]:
        snapshots: list[DocumentSnapshot] = self.db.collection('companies').get()
        for snapshot in snapshots:
            yield CompanyBriefOutModel.create(snapshot.id, snapshot.to_dict(), headers, self)

    def get_company(self, company_id: str, headers: AppHeaders) -> CompanyOutModel:
        ref, snapshot = self._get_company_ref_and_snapshot(company_id)
        if not snapshot.exists:
            raise CompanyNotFoundError(company_id)

        data = snapshot.to_dict()
        return CompanyOutModel.create(company_id, data, headers, self)

    def add_company(self, body: CompanyPostPutModel, headers: AppHeaders) -> CompanyOutModel:
        ref = self.db.collection('companies').document()
        ref.create(body.to_database_dict(headers, self))
        return self.get_company(ref.id, headers)

    def _get_company_ref_and_snapshot(self, company_id) -> tuple[DocumentReference, DocumentSnapshot]:
        ref = self.db.collection('companies').document(company_id)
        snapshot = ref.get()
        if not snapshot.exists:
            raise CompanyNotFoundError(company_id)

        return ref, snapshot


async def get_companies_datastore(db: Client = Depends(get_db_client)):
    return CompaniesDatastore(db)
