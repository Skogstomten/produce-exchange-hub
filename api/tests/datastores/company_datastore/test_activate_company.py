from app.database.mongo.mongo_document_database import MongoDocument
from app.datastores.company_datastore import CompanyDatastore
from app.models.v1.shared import CompanyStatus


def test_activate_company(doc_database_collection_mocks, user_datastore, logger, fake_company_data):
    db, collection = doc_database_collection_mocks
    company_id, company_doc = fake_company_data
    collection.by_id.return_value = MongoDocument(company_doc, collection)

    target = CompanyDatastore(db, user_datastore, logger)
    result = target.activate_company(company_id)

    db.collection.assert_called_with("companies")
    collection.patch_document.assert_called_once_with(company_id, {"status": CompanyStatus.active})
    assert result is not None
