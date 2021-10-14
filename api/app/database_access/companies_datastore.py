from app.database_access.base_datastore import BaseDatastore
from app.database_access.company import Company
from app.database_access.firestore import get_db_client as get_db
from app.errors import NotFoundError


class CompaniesDatastore(BaseDatastore):
    def __init__(self):
        super(CompaniesDatastore, self).__init__(get_db())

    def get_company(self, company_id: str) -> Company:
        document_snapshot = self.db.collection('companies').document(company_id).get()
        if document_snapshot.exists:
            data = document_snapshot.to_dict()
            return Company(document_snapshot.id, data, self)
        raise NotFoundError(company_id)

    def list_companies(self) -> list[Company]:
        company_snapshots = self.db.collection('companies').get()
        for company_snapshot in company_snapshots:
            yield Company(company_snapshot.id, company_snapshot.to_dict(), self)
