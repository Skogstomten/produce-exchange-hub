from unittest.mock import ANY

from app.company.datastores.company_datastore import CompanyDatastore
from tests.fixtures.common_fixtures import get_add_contact_model


def test_add_contact_adds_contact(
    doc_database_collection_mocks,
    user_datastore,
    logger,
    company_id,
    file_manager,
    authenticated_user_default,
):
    db, collection = doc_database_collection_mocks
    add_contact_model = get_add_contact_model()

    target = CompanyDatastore(db, logger)
    target.add_contact(company_id, add_contact_model, authenticated_user_default)

    collection.push_to_list.assert_called_with(company_id, "contacts", ANY)
