"""Tests for CompanyDatastore class."""
from datetime import datetime

import pytest
from pytz import utc

from app.database.mongo.mongo_document_database import MongoDocument
from app.datastores.company_datastore import CompanyDatastore
from app.errors import NotFoundError
from app.models.v1.database_models.company_database_model import ChangeType
from app.models.v1.shared import ContactType


def add_contact_to_company_doc_dict(company_doc_dict, contact_model):
    company_doc_dict["contacts"].append(
        {
            "id": contact_model.id,
            "type": ContactType.email.value,
            "value": "old_email@shit.com",
            "created_by": "user@email.com",
            "created_at": datetime.now(utc),
            "changed_by": None,
            "changed_at": None,
        }
    )


def perform_operation(
    db_collection, user_datastore, logger, fake_company_data, authenticated_user, contact_model, verification_function
):
    db, collection = db_collection
    company_id, company_doc_dict = fake_company_data
    add_contact_to_company_doc_dict(company_doc_dict, contact_model)
    collection.by_id.return_value = MongoDocument(company_doc_dict, collection)
    collection.replace = verification_function

    target = CompanyDatastore(db, user_datastore, logger)
    target.update_contact(company_id, contact_model, authenticated_user)


def test_update_contact_raises_not_found_error_if_company_not_found(
    doc_database_collection_mocks, user_datastore, logger, company_id, authenticated_user_default, contact_model
):
    db, collection = doc_database_collection_mocks
    collection.by_id.return_value = None

    target = CompanyDatastore(db, user_datastore, logger)
    with pytest.raises(NotFoundError, match=f"Company with id '{company_id}' not found"):
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


def test_update_contact_calls_replace(
    doc_database_collection_mocks, user_datastore, logger, fake_company_data, authenticated_user_default, contact_model
):
    db, collection = doc_database_collection_mocks
    company_id, company_doc_dict = fake_company_data
    add_contact_to_company_doc_dict(company_doc_dict, contact_model)
    collection.by_id.return_value = MongoDocument(company_doc_dict, collection)

    target = CompanyDatastore(db, user_datastore, logger)
    target.update_contact(company_id, contact_model, authenticated_user_default)

    collection.replace.assert_called_once()


def test_update_contact_changes_contact(
    doc_database_collection_mocks, user_datastore, logger, fake_company_data, authenticated_user_default, contact_model
):
    def _verify_contact_changed(_, doc_dict):
        contact = next((d for d in doc_dict["contacts"] if d["id"] == contact_model.id), None)
        assert contact["type"] == contact_model.type
        assert contact["value"] == contact_model.value
        assert contact["description"] == contact_model.description
        assert contact["changed_by"] == authenticated_user_default.email
        assert contact["changed_at"].year == datetime.now(utc).year
        assert contact["changed_at"].month == datetime.now(utc).month
        assert contact["changed_at"].day == datetime.now(utc).day

    perform_operation(
        doc_database_collection_mocks,
        user_datastore,
        logger,
        fake_company_data,
        authenticated_user_default,
        contact_model,
        _verify_contact_changed,
    )


def test_update_contact_changes_added(
    doc_database_collection_mocks, user_datastore, logger, fake_company_data, authenticated_user_default, contact_model
):
    def _verify_change_added(_, doc_dict):
        change = next((d for d in doc_dict["changes"]), None)
        assert change is not None
        assert change["path"] == f"contacts.{contact_model.id}"
        assert change["change_type"] == ChangeType.update
        assert change["actor_id"] == authenticated_user_default.id
        assert change["actor_username"] == authenticated_user_default.email

    perform_operation(
        doc_database_collection_mocks,
        user_datastore,
        logger,
        fake_company_data,
        authenticated_user_default,
        contact_model,
        _verify_change_added,
    )
