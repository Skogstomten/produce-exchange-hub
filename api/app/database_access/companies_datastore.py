from datetime import datetime

import pytz
from google.cloud.firestore_v1 import Query

from app import conversion
from app.database_access.address import Address
from app.database_access.base_datastore import BaseDatastore
from app.database_access.company import Company
from app.database_access.firestore import get_db_client as get_db
from app.errors import NotFoundError


class CompaniesDatastore(BaseDatastore):
    def __init__(self):
        super(CompaniesDatastore, self).__init__(get_db())

    def get_company(self, company_id: str, language_iso: str) -> Company:
        document_snapshot = self.db.collection('companies').document(company_id).get()
        if document_snapshot.exists:
            data = document_snapshot.to_dict()
            return Company(document_snapshot.id, data, self, language_iso)
        raise NotFoundError(company_id)

    def list_companies(self,
                       language_iso: str,
                       sort: str | None = None,
                       sort_dir: str = 'desc',
                       start: int = 0,
                       take: int | None = None) -> list[Company]:
        company_refs = self.db.collection('companies')
        query = company_refs.offset(start)

        sort_field_path = self._get_sort_field_path(sort)
        if sort_field_path is not None:
            direction = Query.ASCENDING
            if sort_dir.lower() == 'desc':
                direction = Query.DESCENDING
            query = query.order_by(sort_field_path, direction=direction)

        if take is not None:
            query = query.limit(take)

        company_snapshots = query.stream()
        for company_snapshot in company_snapshots:
            yield Company(company_snapshot.id, company_snapshot.to_dict(), self, language_iso)

    def add_company(self,
                    input_data: dict[str, list],
                    user_id: str,
                    language_iso: str) -> Company:
        company_doc_ref = self.db.collection('companies').document()
        data = {
            'addresses': [],
            'authorized_users': [],
            'company_types': input_data.get('company_types'),
            'content_languages_iso': input_data.get('content_languages_iso'),
            'created_date': datetime.now(pytz.timezone('UTC')),
            'name': {},
            'status': 'unactivated',
        }

        if 'addresses' in input_data:
            for address in input_data.get('addresses'):
                data['addresses'].append(conversion.post_object_to_address_dict(address))

        user = self.db.collection('users').document(user_id)
        data['authorized_users'].append({
            'user': user,
            'roles': ['admin']
        })

        for name in input_data['name']:
            data['name'][name.get('language_iso')] = name.get('name')

        company_doc_ref.create(data)
        return self.get_company(company_doc_ref.id, language_iso)
    #
    # def activate_company(self, company_id: str):
    #     company_ref = self.db.collection('companies').document(company_id)
    #     company_snapshot = company_ref.

    def get_addresses(self,
                      company_id: str,
                      language_iso: str) -> list[Address]:
        company_ref = self.db.collection('companies').document(company_id)
        company_snapshot = company_ref.get(('addresses',))
        if not company_snapshot.exists:
            raise NotFoundError(company_id)

        for address in company_snapshot.to_dict().get('addresses'):
            yield Address(address, self, language_iso)

    def add_address(self,
                    company_id: str,
                    data: dict,
                    language_iso: str) -> Address:
        company_ref = self.db.collection('companies').document(company_id)
        company_snapshot = company_ref.get(('addresses',))
        if not company_snapshot.exists:
            raise NotFoundError(company_id)

        company_data = company_snapshot.to_dict()
        addresses: list[dict] = company_data.get('addresses')
        country_iso = data.get('country_iso')
        country = self.get_localization('countries_iso_name').get(country_iso, country_iso)
        data['country'] = country
        addresses.append(data)
        company_ref.update({'addresses': addresses})
        return Address(data, self, language_iso)

    @staticmethod
    def _get_sort_field_path(sort: str):
        if sort is None:
            return None

        sort = sort.strip().lower()
        if sort == 'date':
            return 'created_date'

        return None
