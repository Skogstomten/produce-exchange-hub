from unittest.mock import Mock, PropertyMock

import pytest
from bson import ObjectId
from pymongo.collection import Collection
from pymongo.results import UpdateResult

from app.company.models.shared.enums import CompanyStatus
from app.database.abstract.document_database import DatabaseCollection
from app.database.mongo.mongo_document_database import MongoDatabaseCollection
from app.shared.errors.errors import NotFoundError


@pytest.fixture
def collection():
    """Fixture for pymongo.collection"""
    update_result = Mock(UpdateResult)
    collection = Mock(Collection)
    collection.update_one.return_value = update_result
    return collection


def get_target(collection, logger):
    doc_id = str(ObjectId())
    target: DatabaseCollection = MongoDatabaseCollection(collection, logger)
    return doc_id, target


def configure_collection(collection, modified_count):
    type(collection.update_one.return_value).modified_count = PropertyMock(return_value=modified_count)


def test_patch_document_document_found(collection, logger):
    configure_collection(collection, 1)

    doc_id, target = get_target(collection, logger)
    target.patch_document(doc_id, {"field_name": "new_value", "enum_val": CompanyStatus.active})

    collection.update_one.assert_called_once_with(
        {"_id": ObjectId(doc_id)},
        {
            "$set": {
                "field_name": "new_value",
                "enum_val": CompanyStatus.active.value,
            }
        },
    )


def test_patch_document_document_not_found(collection, logger):
    configure_collection(collection, 0)
    type(collection).name = PropertyMock(return_value="stuff")

    doc_id, target = get_target(collection, logger)
    with pytest.raises(
        NotFoundError,
        match=f"No document with key='{doc_id}' " f"was found in collection='stuff'",
    ):
        target.patch_document(doc_id, {"key": "value"})
