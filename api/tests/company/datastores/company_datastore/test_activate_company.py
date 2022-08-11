from unittest.mock import Mock, ANY

from app.company.datastores.company_datastore import CompanyDatastore
from app.company.models.shared.enums import CompanyStatus
from app.database.abstract.document_database import DocumentDatabaseUpdateContext
from app.database.mongo.mongo_document_database import MongoDocument


def test_activate_company(
    doc_database_collection_mocks,
    user_datastore,
    logger,
    fake_company_data,
    authenticated_user_default,
    file_manager,
    doc_id,
):
    db, collection = doc_database_collection_mocks
    company_id, company_doc = fake_company_data
    collection.by_id.return_value = MongoDocument(company_doc, collection)
    update_context_mock = Mock(DocumentDatabaseUpdateContext)
    db.update_context.return_value = update_context_mock

    target = CompanyDatastore(db, logger)
    result = target.activate_company(company_id, authenticated_user_default)

    db.collection.assert_called_with("companies")
    update_context_mock.set_values.assert_called_once_with({"status": CompanyStatus.active})
    update_context_mock.push_to_list.assert_called_once_with("changes", ANY)
    collection.update_document.assert_called_once_with(company_id, update_context_mock)
    assert result is not None
