from unittest.mock import Mock, PropertyMock

import pytest
from bson import ObjectId
from pymongo.collection import Collection
from pymongo.results import UpdateResult

from app.database.document_database import DatabaseCollection
from app.database.mongo.mongo_document_database import MongoDatabaseCollection
from app.errors import NotFoundError


@pytest.fixture
def collection():
    update_result = Mock(UpdateResult)
    collection = Mock(Collection)
    collection.update_one.return_value = update_result
    return collection


def test_patch_document_by_id_document_found(collection):
    type(
        collection.update_one.return_value
    ).modified_count = PropertyMock(return_value=1)

    doc_id = ObjectId()
    target: DatabaseCollection = MongoDatabaseCollection(collection)
    target.patch_document(str(doc_id), {"field_name": "new_value"})

    collection.update_one.assert_called_once_with(
        {"_id": doc_id},
        {"$set": {"field_name": "new_value"}},
    )


def test_patch_document_by_id_document_not_found(collection):
    type(
        collection.update_one.return_value
    ).modified_count = PropertyMock(return_value=0)
    type(collection).name = PropertyMock(return_value="stuff")

    doc_id = str(ObjectId())
    target: DatabaseCollection = MongoDatabaseCollection(collection)
    with pytest.raises(
        NotFoundError,
        match=f"No document with key='{doc_id}' "
              f"was found in collection='stuff'"
    ):
        target.patch_document(doc_id, {"key": "value"})
