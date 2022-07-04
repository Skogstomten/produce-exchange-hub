"""Tests for CompanyDatastore class."""
from datetime import datetime
from unittest.mock import Mock

import pytest
from bson import ObjectId
from pytz import utc

from app.database.mongo.mongo_document_database import MongoDocument
from app.datastores.company_datastore import CompanyDatastore
from app.datastores.user_datastore import UserDatastore
from app.dependencies.log import AppLogger
from app.errors import NotFoundError
from app.models.v1.database_models.contact_database_model import ContactDatabaseModel
from app.models.v1.shared import CompanyStatus, ContactType


def _get_id() -> str:
    return str(ObjectId())


def _get_contact_model(
    contact_id: str = _get_id(),
    contact_type: ContactType = ContactType.email,
    value: str = "nisse@perssons.se",
    created_by: str = _get_id(),
    created_at: datetime = datetime.now(utc),
) -> ContactDatabaseModel:
    return ContactDatabaseModel(
        id=contact_id,
        type=contact_type,
        value=value,
        created_by=created_by,
        created_at=created_at,
    )


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
    return _get_contact_model()


@pytest.fixture
def fake_company_data(company_id):
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
        "contacts": [],
    }
    return company_id, fake_doc


def test_activate_company(doc_database_collection_mocks, user_datastore, logger, fake_company_data):
    db, collection = doc_database_collection_mocks
    company_id, company_doc = fake_company_data
    collection.by_id.return_value = MongoDocument(company_doc, collection)

    target = CompanyDatastore(db, user_datastore, logger)
    result = target.activate_company(company_id)

    db.collection.assert_called_with("companies")
    collection.patch_document.assert_called_once_with(company_id, {"status": CompanyStatus.active})
    assert result is not None


def test_add_contact_adds_contact(doc_database_collection_mocks, user_datastore, logger, contact_model, company_id):
    db, collection = doc_database_collection_mocks

    target = CompanyDatastore(db, user_datastore, logger)
    target.add_contact(company_id, contact_model)

    collection.add_to_sub_collection.assert_called_with(company_id, "contacts", contact_model)


def test_update_contact_raises_not_found_error_if_company_not_found(
    doc_database_collection_mocks, user_datastore, logger, company_id, authenticated_user_default, contact_model
):
    db, collection = doc_database_collection_mocks
    collection.by_id.return_value = None

    target = CompanyDatastore(db, user_datastore, logger)
    with pytest.raises(NotFoundError, match=f"Company with id '{company_id}' not found."):
        target.update_contact(company_id, contact_model, authenticated_user_default)


def test_update_contact_raises_not_found_error_if_contact_not_found(
    doc_database_collection_mocks, user_datastore, logger, fake_company_data, authenticated_user_default, contact_model
):
    db, collection = doc_database_collection_mocks
    company_id, company_doc_dict = fake_company_data
    collection.by_id.return_value = MongoDocument(company_doc_dict, collection)

    target = CompanyDatastore(db, user_datastore, logger)
    with pytest.raises(
        NotFoundError, match=f"Contact with id '{contact_model.id}' not found on company '{company_id}'."
    ):
        target.update_contact(company_id, contact_model, authenticated_user_default)
