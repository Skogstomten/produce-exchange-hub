from typing import List

from bson import ObjectId
from fastapi import Depends
from pymongo.database import Database
from pymongo.collection import Collection

from .base_datastore import BaseDatastore
from ..dependencies.app_headers import AppHeaders
from ..dependencies.mongo_db import get_mongo_db
from ..models.companies.company_in_model import CompanyInModel
from ..models.companies.company_out_model import CompanyOutModel
from ..models.companies.company_status import CompanyStatus


class CompaniesDatastore(BaseDatastore[CompanyOutModel]):
    def __init__(self, db: Database):
        super().__init__(db, 'companies')

    def get_companies(self, headers: AppHeaders) -> List[CompanyOutModel]:
        companies: Collection = self.db.get_collection('companies')
        for company in companies.find():
            yield CompanyOutModel.create(str(company['_id']), company, headers, self)

    def get_company(self, company_id: str, headers: AppHeaders) -> CompanyOutModel:
        company = self.db.get_collection('companies').find_one({'_id': ObjectId(company_id)})
        return CompanyOutModel.create(
            company_id,
            company,
            headers,
            self
        )

    def add_company(self, body: CompanyInModel, headers: AppHeaders) -> CompanyOutModel:
        company_id = self.db.get_collection('companies')\
            .insert_one(body.to_database_dict(CompanyStatus.unactivated.value))\
            .inserted_id
        return self.get_company(company_id, headers)

    # def update_company(self, company_id: str, body: CompanyInModel, headers: AppHeaders) -> CompanyOutModel:
    #     ref, snapshot = self._get_ref_and_snapshot(company_id, ('status',))
    #     status: CompanyStatus = snapshot.to_dict().get('status')
    #     ref.set(body.to_database_dict(status))
    #     return self.get_company(company_id, headers)
    #
    # def delete_company(self, company_id: str):
    #     self.delete(company_id)


async def get_companies_datastore(db: Database = Depends(get_mongo_db)):
    return CompaniesDatastore(db)
