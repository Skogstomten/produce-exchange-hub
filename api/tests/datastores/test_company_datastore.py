from datetime import datetime
from unittest.mock import Mock

from bson import ObjectId
from pytz import utc

from app.database.document_database import (
    DocumentDatabase,
    DatabaseCollection,
)
from app.database.mongo.mongo_document_database import MongoDocument
from app.datastores.company_datastore import CompanyDatastore
from app.datastores.user_datastore import UserDatastore
from app.models.v1.shared import CompanyStatus


def test_activate_company():
    doc_id = ObjectId()
    fake_doc = {
        "_id": doc_id,
        "name": {},
        "status": "active",
        "created_date": datetime.now(utc),
        "company_types": [],
        "content_languages_iso": [],
        "description": {},
    }
    collection = Mock(DatabaseCollection)
    collection.by_id.return_value = MongoDocument(fake_doc, collection)
    db = Mock(DocumentDatabase)
    db.collection.return_value = collection
    user_datastore = Mock(UserDatastore)

    target = CompanyDatastore(db, user_datastore)
    result = target.activate_company(str(doc_id))

    db.collection.assert_called_with("companies")
    collection.patch_document.assert_called_once_with(str(doc_id), {"status": CompanyStatus.active})
    assert result is not None
