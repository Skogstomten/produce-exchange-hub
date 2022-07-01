"""Tests for CompanyDatastore class."""
from datetime import datetime
from unittest.mock import Mock

import pytest
from bson import ObjectId
from pytz import utc

from app.database.document_database import (
    DocumentDatabase,
    DatabaseCollection,
)
from app.database.mongo.mongo_document_database import MongoDocument
from app.datastores.company_datastore import CompanyDatastore
from app.datastores.user_datastore import UserDatastore
from app.dependencies.log import AppLogger
from app.models.v1.database_models.contact_database_model import ContactDatabaseModel
from app.models.v1.shared import CompanyStatus, ContactType


def _get_id() -> str:
    return str(ObjectId())


@pytest.fixture
def db_collection():
    """Fixture setting up db mock."""
    collection = Mock(DatabaseCollection)
    db = Mock(DocumentDatabase)
    db.collection.return_value = collection
    return db, collection


@pytest.fixture
def user_datastore():
    """Creates mock for user datastore."""
    mock = Mock(UserDatastore)
    return mock


@pytest.fixture
def logger():
    """Creates logger mock."""
    mock = Mock(AppLogger)
    return mock


@pytest.fixture
def company_id():
    """Creates company id."""
    return _get_id()


@pytest.fixture
def contact_id():
    """Creates contact id."""
    return _get_id()


@pytest.fixture
def contact_model(contact_id):
    """Initiates a contact model."""
    return ContactDatabaseModel(
        id=contact_id,
        type=ContactType.email,
        value="nisse@perssons.se",
        created_by=_get_id(),
        created_at=datetime.now(utc),
    )


@pytest.fixture
def fake_company_document(company_id):
    """Fake document fixture."""
    doc_id = ObjectId(company_id)

    fake_doc = {
        "_id": doc_id,
        "name": {},
        "status": "active",
        "created_date": datetime.now(utc),
        "company_types": [],
        "content_languages_iso": [],
        "description": {},
    }
    return str(doc_id), fake_doc


def test_activate_company(db_collection, user_datastore, logger, fake_company_document):
    db, collection = db_collection
    company_id, company_doc = fake_company_document
    collection.by_id.return_value = MongoDocument(company_doc, collection)

    target = CompanyDatastore(db, user_datastore, logger)
    result = target.activate_company(company_id)

    db.collection.assert_called_with("companies")
    collection.patch_document.assert_called_once_with(company_id, {"status": CompanyStatus.active})
    assert result is not None


def test_add_contact_adds_contact(db_collection, user_datastore, logger, contact_model, company_id):
    db, collection = db_collection

    target = CompanyDatastore(db, user_datastore, logger)
    target.add_contact(company_id, contact_model)

    collection.add_to_sub_collection.assert_called_with(company_id, "contacts", contact_model)
