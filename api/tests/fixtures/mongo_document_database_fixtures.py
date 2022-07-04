"""Contains fixture for mongo document database."""
from unittest.mock import Mock

import pytest
from bson import ObjectId

from app.database.document_database import DatabaseCollection, DocumentDatabase
from app.database.mongo.mongo_document_database import MongoDatabaseCollection, MongoDocument


@pytest.fixture
def mongo_database_collection_mock():
    """Fixture for mock of document collection."""
    return Mock(MongoDatabaseCollection)


@pytest.fixture
def obj_id():
    """Fixture with a random doc id of type bson.ObjectId"""
    return ObjectId()


@pytest.fixture
def doc_id(obj_id):
    """Fixture with random doc id as str."""
    return str(obj_id)


@pytest.fixture
def doc_database_collection_mocks():
    """
    Fixture setting up mock of app.database.document_database.DatabaseCollection.
    :return: Mock(DocumentDatabase)
        with collection.return_value = Mock(DatabaseCollection)
        as tuple[Mock[DocumentDatabase], Mock[DatabaseCollection]]
    """
    collection = Mock(DatabaseCollection)
    db = Mock(DocumentDatabase)
    db.collection.return_value = collection
    return db, collection
